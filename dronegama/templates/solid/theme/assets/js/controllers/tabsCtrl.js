app.controller("TabsCtrl",['$scope', TabsCtrl]);

function TabsCtrl($scope) {
  $scope.tabs = [
      { link : '#/home', label : 'HOME' },
      { link : '#/aboutus', label : 'ABOUT US' },
      { link : '#/drones', label : 'SEARCH DRONES' },
      { link : '#/contactus', label : 'CONTACT US' },
    ]; 
    
  $scope.selectedTab = $scope.tabs[0];    
  $scope.setSelectedTab = function(tab) {
    $scope.selectedTab = tab;
  };
  
  $scope.tabClass = function(tab) {
    if ($scope.selectedTab == tab) {
      return "active";
    } else {
      return "";
    }
  };
};