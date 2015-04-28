var app = angular.module("MyApp", []);

app.controller('ListCtrl', ['$scope', '$http', function($scope, $http) {
    //$scope.data = [];

    $http.get('/api/links')
        .success(function(data, status, headers, config) {
            console.log(data);
            $scope.links = data.links;
        })
        .error(function(data, status, headers, config) {
            console.log(data);
        });
    //$scope.links = ["www.google.com.ar", "www.ole.com.ar"];
}]);