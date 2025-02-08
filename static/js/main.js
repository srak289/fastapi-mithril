import 'mithril'

let root = document.body

const pages = {root: "/", users: "/users", login: "/login"}

let LinksComponent = {
    view: function(vnode) {
        const pages = {root: "/", users: "/users", login: "/login"}
        return m("div", {class: "main"}, [
            m("div", {class: "links-bar"}, Object.entries(pages).map(([k, v]) =>
                m("div", {class: "links-item"},
                    m(m.route.Link, {href: v}, k)
                )
            )),
            vnode.children
        ]);
    }
}

let RootComponent = {
    view: function() {
        return m(LinksComponent, [
            m("h1", {class: "root-component"}, "Test"),
            m("p", {class: "root-component-content"}, "This is content"),
        ]);
    }
}

let UsersComponent = {
    view: function() {
        return m(LinksComponent, {class: "users"}, function() {
            m("h1", {class: "title"}, "Test")
        })
    }
}


m.route(root, "/", {
    "/": RootComponent,
    "/users": LinksComponent,
    "/login": LinksComponent,
})
