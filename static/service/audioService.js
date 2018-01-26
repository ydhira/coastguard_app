(function(){
    "use strict"

    angular.module('guardapp', []).config(function($interpolateProvider) {
             //http://django-angular.readthedocs.org/en/latest/integration.html
             console.log("loading...");
             $interpolateProvider.startSymbol('{$');
             $interpolateProvider.endSymbol('$}');
         });

        // ############## Service Start
        angular.module('guardapp').service('audioService', function($q,$http, $window) {
		    var service = this;
		    console.log('inside audio service');
		    service.uploadFiles = function(audio, callback)
            {
                console.log(audio);
                var formdata = new FormData();
                for (var key in audio){
                     formdata.append(key, audio[key]);
                }
                var request = {
                    method: 'POST',
                    url: '/fileupload/',
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
            };
            service.uploadFile_Query = function(audio , callback){
                var formdata = new FormData();
                for (var key in audio){
                     formdata.append(key, audio[key]);
                }

                // ASK FOR SIMILAR FILE NAMES.
                 var request = {
                    method: 'POST',
                    url: '/getsimilaraudio/',
                    data: formdata,
                    headers: {
                        'Content-Type': undefined
                    }
                };

                $http(request)
                    .success(function (d, status) {
                        callback(null, d);
                    })
                    .error(function (error, status) {
                        callback(error, null);
                   });

            };
        });



})();