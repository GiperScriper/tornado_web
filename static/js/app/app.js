var myModule = angular.module('myModule', []);
        
myModule.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{(');
  $interpolateProvider.endSymbol(')}');
});

myModule.controller('MyCtrl', MyCtrl);

function MyCtrl($scope) {
    $scope.items = {
        'name': 'Mike',
        'age': 25
    }
};

myModule.controller('LoginCtrl', function ($scope) {
    var data = {'data':'your data'};
    $scope.user = {
        email: 'my@test.ru',
        name: 'Nick'
    };

    $scope.items = [
        { name: 'PHP' },
        { name: 'Python '},
        { name: 'Perl' }
    ];
    console.log(data);
    console.log($scope.user);
});