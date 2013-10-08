var assert = require('assert');
var fs = require('fs');
var path = require('path');
var jsdom = require('jsdom').jsdom;

describe('map', function() {
  var map = null;

  before(function(done) {
    jsdom.env({
      file: 'public/index.html',
      features: {
        FetchExternalResources: ['script'],
      },
      done: function(error, window) {
        if (error) console.log(error);
        window.document.addEventListener('DOMContentLoaded', function() {
          // `window.map` is the map code
          map = window.map;
          done();
        });
      }
    });
  });

  describe('_findFillColorPrecinct()', function() {
    it('Returns the tie color if there are no candidates', function() {
      var candidates = [];

      assert.equal(map._findFillColorPrecinct(candidates), map.tieColor);
    });
  });

  describe('formatPercent()', function() {
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(1), 100);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0), 0);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0.001), 0);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0.005), 1);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0.01), 1);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0.9949), 99);
    });
    it('Multiplies by 100 and rounds to two decimal places', function() {
      assert.equal(map.formatPercent(0.995), 100);
    });
  });

  describe('formatAddress()', function() {
    it('Leaves addresses with `Minneapolis` in them alone', function() {
      assert.equal(
        map.formatAddress('111 Hennepin Ave, Minneapolis'),
        '111 Hennepin Ave, Minneapolis'
      );
    });
    it('Leaves addresses with `Minneapolis` in them alone', function() {
      assert.equal(
        map.formatAddress('111 Hennepin Ave, minneapolis'),
        '111 Hennepin Ave, minneapolis'
      );
    });
    it('Appends `Minneapolis, MN` to addresses without `Minneapolis` already in them', function() {
      assert.equal(
        map.formatAddress('111 Hennepin Ave'),
        '111 Hennepin Ave Minneapolis, MN'
      );
    });
    it('Leave zip codes alone', function() {
      assert.equal(
        map.formatAddress('55455'),
        '55455'
      );
    });
    it('Leave zip codes alone', function() {
      assert.equal(
        map.formatAddress('55455 Hennepin Ave'),
        '55455 Hennepin Ave Minneapolis, MN'
      );
    });

  });

});

