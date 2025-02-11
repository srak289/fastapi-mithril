import 'mithril'
import cytoscape from 'cytoscape';

let root = document.body

let LinksComponent = {
    view: function(vnode) {
        return m("div", {class: "main"}, [
            m("div", {class: "links-bar"}, Object.entries(pages).map(([k, v]) =>
                m("div", {class: "links-item", onclick: () => m.route.set(k)},
                    m("h3", {class: "links-text"}, v.title)
                )
            )),
            vnode.children
        ]);
    }
}

let MainComponent = {
    title: "Home",
    view: function() {
        return m(LinksComponent, m("div", {class: "home-component"}, [
            m("h1", {class: "home-component-title"}, "Welcome"),
            m("p", {class: "home-component-content"}, "Click the Cytoscape tab to view a graph"),
        ]));
    }
}

let Graph = {
    model: {},
    fetch: function() {
        m.request({
            method: "GET",
            url: "/api/v1/nodes",
        })
        .then(function(result) {
            Graph.model = result
        });
    },
}

let CytoscapeComponent = {
    title: "Cytoscape",
    cy: null,
    dblClickHandler(evt) {
        evt.cy.animate({
            fit: {eles: evt.target, padding: 50},
            duration: 500,
            easing: 'ease-in-out',
        });
    },
    setup() {
        CytoscapeComponent.cy = cytoscape({
            container: document.getElementById("cy"),
            elements: Graph.model.elements,
            style: [
              {
                selector: 'node',
                style: {
                  'background-color': '#3498db',
                  'label': 'data(id)'
                }
              },
              {
                selector: 'edge',
                style: {
                  'width': 2,
                  'line-color': '#ccc'
                }
              }
            ],
            layout: { name: 'cose', animated: false },
            wheelSensitivity: 0.05,
        });
        CytoscapeComponent.cy.on("vdblclick", CytoscapeComponent.dblClickHandler);
    },
    view: function() {
        return m(LinksComponent, m("div", {class: "cytoscape-component"}, [
            m("div", {id: "cy", class: "cytoscape-canvas"}),
            m("button", {onclick: () => CytoscapeComponent.cy.animate({
                fit: { padding: 20 },
                duration: 500,
                easing: 'ease-in-out',
            })}, "Fit"),
            m("button", {onclick: () => {
                CytoscapeComponent.cy.elements().remove();
                CytoscapeComponent.setup();
            }}, "Redraw"),
            m("button", {onclick: () => {
                CytoscapeComponent.cy.elements().remove();
                Graph.fetch();
                CytoscapeComponent.setup();
            }}, "Renew"),
            m("p", "Double-click to zoom to a node"),
        ]));
    },
    oninit: Graph.fetch,
    oncreate: function() {
        CytoscapeComponent.setup();
    },
    onbeforeremove: function() {
        CytoscapeComponent.cy.destroy();
    }
}

let pages = {
    "/": MainComponent,
    "/cy": CytoscapeComponent,
}

m.route(root, "/", pages);
