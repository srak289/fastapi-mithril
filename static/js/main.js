import 'mithril'

let root = document.body

let RootComponent = {
    view: function() {
        return m("h1", {class: "title"}, "Test")
    }
}

m.route(root, "/", {
    "/": RootComponent,
})
