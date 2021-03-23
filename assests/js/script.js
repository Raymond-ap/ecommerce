/* 
===========  Dialog  =========== 
*/
(function($) {

    "use strict";

    // Version = 1.0

    var defaults = {
        overlay: true,
        classes: 'show',
        place: '',
        
    };

    $.fn.toggleDialog = function(options) {
        var settings = $.extend ( {}, defaults, options );

        return this.each(function() {
            var self = $(this), s = settings, o, oEl, t = self.data('target');

            self.on('click', function() {
                $(t).toggleClass(s.classes);

                if( s.overlay ) {
                    o = $('<div class="overlay"></div>');
                    $('body').append(o);

                    oEl = $('.overlay');
                }

                if( oEl !== undefined ) {
                    oEl.on('click', function() {
                        $(t).removeClass(s.classes);
                        $(this).fadeOut().remove();
                    });
                }

            });

        });
    }

    $.fn.dismissDialog = function() {
        return this.each(function() {
            var self = $(this), t = self.data('dismiss');

            self.on('click', function() {
                $( '.' + t ).removeClass('show');

                if( $('.overlay') ) {
                    $('.overlay').fadeOut().remove();
                }
            });
        });
    }

    $(window).on('resize', function() {
        $('.charm').removeClass('show');

        if( $('.overlay') ) {
            $('.overlay').fadeOut().remove();
        }
    });

    // Call plugin
    $('[data-dismiss="charm"]').dismissDialog();
    $('[data-role="charm"]').toggleDialog();

})(jQuery);

// Selected 
(function($) {

    $('[data-role="selected"]').each(function() {
        var $that = $(this), opt = $that.data('multiple'), $target = $that.find('.select-target');

        if (opt === "yes" || opt === "YES") {
            $target.click(function() {
                $(this).toggleClass('selected');
            });
        }
        else if (opt === "no" || opt === "NO") {
            $target.click(function() {
                $(this).toggleClass('selected').siblings().removeClass('selected');
            });
        }
    });

})(jQuery);

$(document).ready(function() {
    // Back to top
    var backTop = $(".back-to-top");

    $(window).scroll(function() {
        if($(document).scrollTop() > 400) {
            backTop.css('visibility', 'visible');
        }
        else if($(document).scrollTop() < 400) {
            backTop.css('visibility', 'hidden');
        }
    });

    backTop.click(function() {
        $('html').animate({
            scrollTop: 0
        }, 1000);
        return false;
    });

    // Clone Navigation
    var $mNav = $('#mobileNav').html();

    $('.mobile-menu').html($mNav);

    // Tooltip
    $('[data-toggle="tooltip"]').tooltip();

    $('.product-carousel').owlCarousel({
        loop: false,
        dots: false,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            900: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });

    // Modal Product
    $('#filterProduct').on('show.bs.modal', function(event) {
        var $that = $(event.relatedTarget), $el = $that.next().html();

        var $modal = $(this);

        $modal.find('.modal-body').html($el);

        return $modal;
    });

    var thumb = $('.product-single').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: true,
        navText: ["<span class='icon-angle-left'></span>", "<span class='icon-angle-right'></span>"],
        onTranslate: function(event) {
            $('.product-single-thumb .product-item').eq(event.page.index).addClass('active').siblings().removeClass('active');
        },
    });
    
    $('.product-single-thumb').on('click', '.product-item', function() {
        var index = $(this).index();
        thumb.trigger('to.owl.carousel', [index, 300]);
    });

    $('.number-input').each(function() {
        var $this = $(this), $input = $this.children('input'), $val = $input.val();

        var minVal = $input.attr('min');
        var maxVal = $input.attr('max');

        var btnInc = $this.children('.btn-increase');
        var btnDec = $this.children('.btn-decrease');

        if(!$input.val()) {
            $input.val(0);
        }

        btnDec.click(function() {
            $val = $input.val();
            if ($val > parseInt(minVal)) {
                $input.val(+ $val - 1);
            }
        });

        btnInc.click(function() {
            $val = $input.val();
            if ($val < parseInt(maxVal)) {
                $input.val(+ $val + 1);
            }
        });

    });

    $('[data-toggle-class]').each(function() {
        var $cls = $(this).data('toggle-class');
        $(this).click(function() {
            $(this).toggleClass($cls);
        });
    });

    $('.toggle-account-switch').click(function() {
        var par = $(this).parents('.account-switch');
        par.removeClass('active').siblings().addClass('active');
    });
});