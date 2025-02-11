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

let RootComponent = {
    title: "Root",
    view: function() {
        return m(LinksComponent, m("div", {class: "root-component"}, [
            m("h1", {class: "root-component-title"}, "Test"),
            m("p", {class: "root-component-content"}, "This is content"),
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
    view: function() {
        return m(LinksComponent, m("div", {class: "cytoscape-component"}, [
            m("div", {id: "cy", class: "cytoscape-canvas"}),
            m("button", {onclick: () => CytoscapeComponent.cy.animate({
                fit: { padding: 20 },
                duration: 500,
                easing: 'ease-in-out',
            })}, "Fit"),
            m("p", "Double-click to zoom to a node"),
        ]));
    },
    oninit: Graph.fetch,
    oncreate: function(vnode) {
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
            layout: { name: 'cose' },
            wheelSensitivity: 0.05,
        });
        CytoscapeComponent.cy.on("vdblclick", CytoscapeComponent.dblClickHandler);
    }   
}

let UsersComponent = {
    title: "Users",
    view: function() {
        return m(LinksComponent, m("div", {class: "users-component"}, [
            m("h1", {class: "users-component-title"}, "Users"),
        ]));
    }
}

let LoginComponent = {
    title: "Login",
    view: function() {
        return m(LinksComponent, m("div", {class: "login-component"}, [
            m("h1", {class: "login-component-title"}, "Login"),
        ]));
    }
}


let pages = {
    "/": RootComponent,
    "/cy": CytoscapeComponent,
    "/users": UsersComponent,
    "/login": LoginComponent,
}

m.route(root, "/", pages);
