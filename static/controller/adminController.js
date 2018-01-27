(function(){
    "use strict";

    angular.module('guardapp').directive('ngFiles',['$parse', function ($parse) {
            function fn_link(scope, element, attrs) {
                var onChange =  $parse(attrs.ngFiles);
                element.on('change', function (event) {
                    onChange(scope, { $files: event.target.files });
                });
            };

            return{
                link: fn_link
            }
        }]);

            // ############## Contorller Start
    angular.module('guardapp').controller('adminController', function(audioService, $scope,$location, $window){

            var controller = this;
            console.log('inside admin controller');
            controller.audio_file = {};
            controller.file = null;
            controller.similar_audios = [];

            var formdata = new FormData();
            this.print = function(){
                console.log("HELLO!");
            };

            $scope.getTheFiles = function ($files) {
                controller.file = $files[0];
                console.log('files attached: ', $files.length );
                angular.forEach($files, function (value, key) {
                    formdata.append(key, value);
                });
            };

            controller.uploadFiles = function () {
                console.log('inside upload file func');
                controller.audio_file.name =  formdata.get('0').name;
                controller.audio_file.audio_file = controller.file;
                console.log(controller.audio_file);
                audioService.uploadFiles(controller.audio_file, function(err, data){
                    if (err){
                        console.log('Error while uploading files');
                    }
                    else{
                        console.log('success loading files');
                        // $window.location.href = '/upload/'
                    }
                });
                controller.audio_file = {};
            };

            controller.uploadFile_Query = function() {
                console.log('uploadFile_Query');
                controller.audio_file.name =  formdata.get('0').name;
                controller.audio_file.audio_file = controller.file;
                audioService.uploadFile_Query(controller.audio_file, function(err, data){
                    if (err){
                        console.log(err);
                        console.log('Error while uploading files_query');
                    }
                    else{
                       console.log(data);
//                        console.log(JSON.parse(data));
//                        console.log(typeof(data[0].fields.audio_file));
//                        data = JSON.parse(data[0].fields.audio_file);
                        controller.similar_audios = data;
//                        controller.similar_audios.push(data);
//                         $window.location.href = '/audio/';
//                        $window.document.body.parentNode.innerHTML = data;
//                        document.getElementById("content").innerHTML=data;

                        console.log('Successfully uploaded and queried file');
//                        console.log(controller.similar_audios);
                    }
                });
                controller.audio_file = {};
            };

        });

})();