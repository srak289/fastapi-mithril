import 'mithril'
import cytoscape from 'cytoscape';

let root = document.body

const pages = {
    Root: "/",
    Cytoscape: "/cy",
    Users: "/users",
    Login: "/login",
}

let LinksComponent = {
    view: function(vnode) {
        return m("div", {class: "main"}, [
            m("div", {class: "links-bar"}, Object.entries(pages).map(([k, v]) =>
                m("div", {class: "links-item", onclick: () => m.route.set(v)},
                    m("h3", {class: "links-text"}, k)
                )
            )),
            vnode.children
        ]);
    }
}

let RootComponent = {
    view: function() {
        return m(LinksComponent, m("div", {class: "root-component"}, [
            m("h1", {class: "root-component-title"}, "Test"),
            m("p", {class: "root-component-content"}, "This is content"),
        ]));
    }
}

let CytoscapeComponent = {
    view: function() {
        return m(LinksComponent, m("div", {class: "cytoscape-component"}, [
            m("div", {id: "cy", class: "cytoscape-canvas"}),
        ]));
    },
    oncreate: function(vnode) {
        var cy = cytoscape({
            container: document.getElementById("cy"),
            elements: [
                { data: { id: "a" } },
                { data: { id: "b" } },
                { data: { id: "c" } },
                { data: { id: "ab", source: "a", target: "b" } },
                { data: { id: "ac", source: "a", target: "c" } },
            ],
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
            layout: { name: 'grid' },
        });
    }   
}

let UsersComponent = {
    view: function() {
        return m(LinksComponent, m("div", {class: "users-component"}, [
            m("h1", {class: "users-component-title"}, "Users"),
        ]));
    }
}

let LoginComponent = {
    view: function() {
        return m(LinksComponent, m("div", {class: "login-component"}, [
            m("h1", {class: "login-component-title"}, "Login"),
        ]));
    }
}


m.route(root, "/", {
    "/": RootComponent,
    "/cy": CytoscapeComponent,
    "/users": UsersComponent,
    "/login": LoginComponent,
})
