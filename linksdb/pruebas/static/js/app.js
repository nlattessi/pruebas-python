var app = angular.module("app", []);

app.controller("AppCtrl", function($http) {
    var app = this;

    $http.get("/api/link").success(function(data) {
        app.links = data.objects;
    });

    app.addLink = function() {
        $http.post("/api/link", {"url":"http://www.google.com.ar", "descripcion":"el google de la gente"})
            .success(function(data) {
                app.links.push(data);
            })
            .error(function(err) {
                console.log(err);
            });
    };

    app.deleteLink = function(link) {
        console.log(link.id);
        $http.delete("/api/link/" + link.id).success(function(response) {
            console.log(response);
            app.links.splice(app.links.indexOf(link), 1);
        });
    };

    app.updateLink = function(link) {
        console.log(link);
        $http.put("/api/link/" + link.id, link).error(function(err) {
            console.log(err);
        });
    };
});