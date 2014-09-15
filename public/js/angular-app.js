'use strict';

/* App level module */

angular.module('vpt', [
  'vptFilters',
  'vptControllers'
]);

/* Controllers */

var vptControllers = angular.module('vptControllers', []);

vptControllers.controller('SeasonResultsCtrl', ['$scope', '$attrs', '$http',
  function($scope, $attrs, $http) {

    var AggregatedResult = function(playerName) {
      this._playerName = playerName;
      this._scores = [];
    };

    AggregatedResult.prototype = {

      getPlayerName: function() {
        return this._playerName;
      },
      getScores: function() {
        return this._scores;
      },
      addScore: function(score) {
        this._scores.push(score);
      },
      getTotalScore: function() {
        return this._scores.reduce(function(a, b) {
          return a + b;
        });
      },
      getLowestScore: function() {
        return Math.min.apply(Math, this._scores);
      },
      getLowestScoreIndex: function() {
        return this._scores.indexOf(this.getLowestScore());
      },
      getAdjustedScore: function() {
        return this.getTotalScore() - this.getLowestScore();
      }
    };

    $scope.aggregatedResults = [];
    $scope.shouldDiscardLowestScore = false;
    $scope.resultsFetchStatus = "Chargement des données...";

    $http.get('/season/' + $attrs.seasonId + '/results').success(function(response) {

      $scope.numberOfTournaments = response.results.length;
      $scope.resultsFetchStatus = ($scope.numberOfTournaments ? "Affichage en cours..." : "Pas encore de données enregistrées !");

      angular.forEach(response.players, function(playerName, playerId) {
        var aggregatedResult = new AggregatedResult(playerName);
        angular.forEach(response.results, function(result) {
          aggregatedResult.addScore(result[playerId] ? result[playerId] : 0);
        });
        $scope.aggregatedResults.push(aggregatedResult);
      });

    }).error(function(response) {
      $scope.resultsFetchStatus = "Erreur de chargement des résultats : " + response;
    });
  }
]);

/* Filters */

var vptFilters = angular.module('vptFilters', []);

vptFilters.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i = 0; i < total; i++)
      input.push(i);
    return input;
  };
});

vptFilters.filter('rank', function() {
  return function(input) {
    var suffix = (input === 1 ? "er" : "e");
    return input + suffix;
  };
});