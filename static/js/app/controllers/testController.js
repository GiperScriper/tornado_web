

main.factory('NotesFactory', function ($resource) {
	return $resource('http://localhost:8889/notes/:id', {id: '@id'}, {
		GETF: {
			method: 'GET'
		},
		UPDATE2: {
			method: 'PUT'
		}
	});
});

main.controller('testController', function ($scope, NotesFactory) {
	NotesFactory.GETF().$promise.then(
		function (data) {
			console.log('success');
			console.log(data.data);
			$scope.notes = data.data;
		},
		function (error) {
			console.log(error.statusText);
		}
	);
	var sample = {'sample':'sample'};
	NotesFactory.UPDATE2(sample).$promise.then(
		function (data) {
			console.log('success');
			console.log(data);
		},
		function (error) {
			console.log(error);
		}
	);
});