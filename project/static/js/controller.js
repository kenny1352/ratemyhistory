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
   // $scope.search = '';
   // $scope.found = [];
   
   
   socket.on('message', function(msg) {
      console.log(msg);
      $scope.messages.push(msg);
      $scope.$apply();
      var elem = document.getElementById('msgpane');
      elem.scrollTop = elem.scrollHeight;
       
   });
   
  
   // $scope.send = function(){
   $scope.send = function send(){   
      console.log('Sending message: ', $scope.text);
      socket.emit('massage', $scope.text);
      // socket.emit('message', {'text' : $scope.text});
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
      // $scope.password = '';
      socket.emit('login', $scope.password); //Maddy Added this and commented the line above 
      console.log("logged in", $scope.name);
   };
   // Maddy added this
       $scope.setName2 = function setName2() {
  
        socket.emit('identify', $scope.name2);
        $scope.name = $scope.name2;
        $scope.$apply();
        socket.emit('identify', $scope.name2)
       };
   
   
   socket.on('logged', function(data) {
      logged_in = data['logged_in'];
      //user = data['username']
      console.log("checking login");
      if (logged_in == 1) {
         console.log("logged in");
         $scope.password = '';
         $scope.loggedIn = 'false';
         //$scope.user=data['username'];
         //console.log('user', $scope.user);
         $("#logout_button").show();
         $("#login_button").hide();
         $("#send_button").show();
         $("#chatText").show();
         $("#msgpane").show();
         $scope.$apply();
      } else {
         console.log("logged out");
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
      //login('hide');
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