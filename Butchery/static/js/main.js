/**
 * main.js
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2015, Codrops
 * http://www.codrops.com
 */
;
(function (window) {

    'use strict';

    var support = {
            animations: Modernizr.cssanimations
        },
        animEndEventNames = {
            'WebkitAnimation': 'webkitAnimationEnd',
            'OAnimation': 'oAnimationEnd',
            'msAnimation': 'MSAnimationEnd',
            'animation': 'animationend'
        },
        animEndEventName = animEndEventNames[Modernizr.prefixed('animation')],
        onEndAnimation = function (el, callback) {
            var onEndCallbackFn = function (ev) {
                if (support.animations) {
                    if (ev.target != this) return;
                    this.removeEventListener(animEndEventName, onEndCallbackFn);
                }
                if (callback && typeof callback === 'function') {
                    callback.call();
                }
            };
            if (support.animations) {
                el.addEventListener(animEndEventName, onEndCallbackFn);
            } else {
                onEndCallbackFn();
            }
        };

    // from http://www.sberry.me/articles/javascript-event-throttling-debouncing
    function throttle(fn, delay) {
        var allowSample = true;

        return function (e) {
            if (allowSample) {
                allowSample = false;
                setTimeout(function () {
                    allowSample = true;
                }, delay);
                fn(e);
            }
        };
    }

    // sliders - flickity
    var sliders = [].slice.call(document.querySelectorAll('.slider')),
        // array where the flickity instances are going to be stored
        flkties = [],
        // grid element
        grid = document.querySelector('.grid'),
        // isotope instance
        iso,
        // filter ctrls
        filterCtrls = [].slice.call(document.querySelectorAll('.filter > button')),
        // cart
        cart = document.querySelector('.cart'),
        cartItems = cart.querySelector('.cart__count');

    function init() {
        // preload images
        imagesLoaded(grid, function () {
            initFlickity();
            initIsotope();
            initEvents();
            classie.remove(grid, 'grid--loading');
        });
    }

    function initFlickity() {
        sliders.forEach(function (slider) {
            var flkty = new Flickity(slider, {
                prevNextButtons: false,
                wrapAround: true,
                cellAlign: 'left',
                contain: true,
                resize: false
            });

            // store flickity instances
            flkties.push(flkty);
        });
    }

    function initIsotope() {
        iso = new Isotope(grid, {
            isResizeBound: false,
            itemSelector: '.grid__item',
            percentPosition: true,
            masonry: {
                // use outer width of grid-sizer for columnWidth
                columnWidth: '.grid__sizer'
            },
            transitionDuration: '0.6s'
        });
    }

    function initEvents() {
        filterCtrls.forEach(function (filterCtrl) {
            filterCtrl.addEventListener('click', function () {
                classie.remove(filterCtrl.parentNode.querySelector('.filter__item--selected'), 'filter__item--selected');
                classie.add(filterCtrl, 'filter__item--selected');
                iso.arrange({
                    filter: filterCtrl.getAttribute('data-filter')
                });
                recalcFlickities();
                iso.layout();
            });
        });

        // window resize / recalculate sizes for both flickity and isotope/masonry layouts
        window.addEventListener('resize', throttle(function (ev) {
            recalcFlickities()
            iso.layout();
        }, 50));

        // add to cart
		[].slice.call(grid.querySelectorAll('.grid__item')).forEach(function (item) {
            item.querySelector('.action--buy').addEventListener('click', addToCart);
        });
    }

    function addToCart() {
        classie.add(cart, 'cart--animate');
        setTimeout(function () {
            cartItems.innerHTML = Number(cartItems.innerHTML) + 1;
        }, 200);
        onEndAnimation(cartItems, function () {
            classie.remove(cart, 'cart--animate');
        });
    }

    function recalcFlickities() {
        for (var i = 0, len = flkties.length; i < len; ++i) {
            flkties[i].resize();
        }
    }

    init();

})(window);

(function () {

    var viewEl = document.querySelector('.view'),
        gridEl = viewEl.querySelector('.grid'),
        items = [].slice.call(gridEl.querySelectorAll('.product')),
        basket;

    // the compare basket
    function CompareBasket() {
        this.el = document.querySelector('.compare-basket');
        this.compareCtrl = this.el.querySelector('.action--compare');
        this.compareWrapper = document.querySelector('.compare'),
            this.closeCompareCtrl = this.compareWrapper.querySelector('.action--close')

        this.itemsAllowed = 3;
        this.totalItems = 0;
        this.items = [];

        // compares items in the compare basket: opens the compare products wrapper
        this.compareCtrl.addEventListener('click', this._compareItems.bind(this));
        // close the compare products wrapper
        var self = this;
        this.closeCompareCtrl.addEventListener('click', function () {
            // toggle compare basket
            classie.add(self.el, 'compare-basket--active');
            // animate..
            classie.remove(viewEl, 'view--compare');
        });
    }

    CompareBasket.prototype.add = function (item) {
        // check limit
        if (this.isFull()) {
            return false;
        }

        classie.add(item, 'product--selected');

        // create item preview element
        var preview = this._createItemPreview(item);
        // prepend it to the basket
        this.el.insertBefore(preview, this.el.childNodes[0]);
        // insert item
        this.items.push(preview);

        this.totalItems++;
        if (this.isFull()) {
            classie.add(this.el, 'compare-basket--full');
        }

        classie.add(this.el, 'compare-basket--active');
    };

    CompareBasket.prototype._createItemPreview = function (item) {
        var self = this;

        var preview = document.createElement('div');
        preview.className = 'product-icon';
        preview.setAttribute('data-idx', items.indexOf(item));

        var removeCtrl = document.createElement('button');
        removeCtrl.className = 'action action--remove';
        removeCtrl.innerHTML = '<i class="fa fa-remove"></i><span class="action__text action__text--invisible">Remove product</span>';
        removeCtrl.addEventListener('click', function () {
            self.remove(item);
        });

        var productImageEl = item.querySelector('img.product__image').cloneNode(true);

        preview.appendChild(productImageEl);
        preview.appendChild(removeCtrl);

        var productInfo = item.querySelector('.product__info').innerHTML;
        preview.setAttribute('data-info', productInfo);

        return preview;
    };

    CompareBasket.prototype.remove = function (item) {
        classie.remove(this.el, 'compare-basket--full');
        classie.remove(item, 'product--selected');
        var preview = this.el.querySelector('[data-idx = "' + items.indexOf(item) + '"]');
        this.el.removeChild(preview);
        this.totalItems--;

        var indexRemove = this.items.indexOf(preview);
        this.items.splice(indexRemove, 1);

        if (this.totalItems === 0) {
            classie.remove(this.el, 'compare-basket--active');
        }

        // checkbox
        var checkbox = item.querySelector('.action--compare-add > input[type = "checkbox"]');
        if (checkbox.checked) {
            checkbox.checked = false;
        }
    };

    CompareBasket.prototype._compareItems = function () {
        var self = this;

        // remove all previous items inside the compareWrapper element
		[].slice.call(this.compareWrapper.querySelectorAll('div.compare__item')).forEach(function (item) {
            self.compareWrapper.removeChild(item);
        });

        for (var i = 0; i < this.totalItems; ++i) {
            var compareItemWrapper = document.createElement('div');
            compareItemWrapper.className = 'compare__item';

            var compareItemEffectEl = document.createElement('div');
            compareItemEffectEl.className = 'compare__effect';

            compareItemEffectEl.innerHTML = this.items[i].getAttribute('data-info');
            compareItemWrapper.appendChild(compareItemEffectEl);

            this.compareWrapper.insertBefore(compareItemWrapper, this.compareWrapper.childNodes[0]);
        }

        setTimeout(function () {
            // toggle compare basket
            classie.remove(self.el, 'compare-basket--active');
            // animate..
            classie.add(viewEl, 'view--compare');
        }, 25);
    };

    CompareBasket.prototype.isFull = function () {
        return this.totalItems === this.itemsAllowed;
    };

    function init() {
        // initialize an empty basket
        basket = new CompareBasket();
        initEvents();
    }

    function initEvents() {
        items.forEach(function (item) {
            var checkbox = item.querySelector('.action--compare-add > input[type = "checkbox"]');
            checkbox.checked = false;

            // ctrl to add to the "compare basket"
            checkbox.addEventListener('click', function (ev) {
                if (ev.target.checked) {
                    if (basket.isFull()) {
                        ev.preventDefault();
                        return false;
                    }
                    basket.add(item);
                } else {
                    basket.remove(item);
                }
            });
        });
    }

    init();

})();
