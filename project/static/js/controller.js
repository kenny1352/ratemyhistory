var ISSChatApp = angular.module('ISSChatApp', []);

/*
function login(showhide){
   if(showhide == "show"){
      document.getElementById('popupbox').style.visibility="visible";
   }else if(showhide == "hide"){
      document.getElementById('popupbox').style.visibility="hidden"; 
   }
}    */


ISSChatApp.controller('ChatController', function($scope) {
   var socket = io.connect('https://' + document.domain + ':' 
   +location.port + '/iss');
   
   $scope.messages = [];
   $scope.name = '';
   $scope.email = '';
   $scope.password = '';
   $scope.user='';
   $scope.text = '';
   $scope.keepMsgUp = 0;
   // $scope.search = '';
   // $scope.found = [];
   
   
   socket.on('message', function(msg) {
      console.log(msg);
      $scope.messages.push(msg);
      $scope.$apply();
      var elem = document.getElementById('msgpane');
      elem.scrollTop = elem.scrollHeight;
       
   });
   
  
   $scope.send = function(){
      console.log('Sending message: ', $scope.text);
      socket.emit('message',$scope.text);
      $scope.text = '';
   };
   
   
   //GETTING RID OF THIS DONT CHANGE YET
   $scope.processLogin = function () {
      console.log("Trying to log in");
      //login('hide');
      // var temp = $('email').val();
      // var temp2 = $('password').val();
      //socket.emit('userLogin', {'email' : $scope.email, 'password' : $scope.password});
      // socket.emit('userLogin', {'email' : temp, 'password' : temp2});
      console.log("After login emit");
      $scope.password = '';
   };
   
   socket.on('logged', function(data) {
      logged_in = data['logged_in'];
      user = data['username']
      console.log("checking login");
      console.log("user is: " + user)
      if (logged_in == 1) {
         console.log("logged in");
         $scope.password = '';
         $scope.loggedIn = 'false';
         $scope.keepMsgUp = 1;
         $scope.user=data['username'];
         //console.log('user', $scope.user);
         $("#logout_button").show();
         $("#login_button").hide();
         if ($scope.keepMsgUp == 1 && $scope.user != ''){
            $("#send_button").show();
            $("#chatText").show();
            $("#msgpane").show();
         }
         $scope.$apply();
      } else {
         console.log("logged out");
         $scope.keepMsgUp = 0;
         $("#logout_button").hide();
         $("#login_button").show();
         $("#send_button").hide();
         $("#chatText").hide();
         $("#msgpane").hide();
         $scope.name2 = '';
         $scope.password = '';
         $scope.loggedIn = '';
         $scope.$apply();
      }
      console.log($scope.loggedIn);
   });
   

   $scope.logout = function() {
      console.log("logging out");
      $scope.keepMsgUp = 0;
      $scope.name2 = '';
      socket.emit('logout', {});
      //$scope.$apply();
   };
   
   
   socket.on('connect', function() {
      console.log('connected'); 
      
      $("#send_button").hide();
      $("#chatText").hide();
      $("#msgpane").hide();
      
   });
   
});