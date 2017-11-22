(function(){
    "use strict"

    angular.module('guardapp', [])
        .config(function($interpolateProvider) {
             //http://django-angular.readthedocs.org/en/latest/integration.html
             $interpolateProvider.startSymbol('{$');
             $interpolateProvider.endSymbol('$}');
         })

        .directive('ngFiles',['$parse', function ($parse) {
            function fn_link(scope, element, attrs) {
                var onChange =  $parse(attrs.ngFiles);
                element.on('change', function (event) {
                    onChange(scope, { $files: event.target.files });
                });
            };

            return{
                link: fn_link
            }
        }])

        // ############## Contorller Start
        .controller('adminController',function(audioService, $scope,$location, $window){

            var controller = this;
            var formdata = new FormData();
            $scope.getTheFiles = function ($files) {
                angular.forEach($files, function (value, key) {
                    formdata.append(key, value);
                });
                console.log(formdata.get('0'));
            };

            controller.uploadFiles = function () {
                audioService.uploadFiles(formdata, function(err, data){
                    if (err){
                        console.log('Error while uploading files');
                    }

                    else{
                        console.log('success loading files');
                    }

                });
            };

        })

        // ############## Service Start
		.service('audioService', function($q,$http, $window) {
		    var service = this;
		    service.uploadFiles = function(formdata, callback)
            {
                console.log(formdata)
                var request = {
                    method: 'POST',
                    url: 'fileupload/',
                    data: formdata,
                    headers: {
                        'Content-Type': undefined
                    }
                };
                // SEND THE FILES.
                $http(request)
                    .success(function (d, status) {
                        callback(null, d);
                    })
                    .error(function (error, status) {
                        callback(error, null);
                    });

            }
        });

})();