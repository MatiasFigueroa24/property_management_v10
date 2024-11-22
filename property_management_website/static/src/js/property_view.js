odoo.define('property_management_website.property_management_website1', function (require) {
    var odoo = require('web.ajax');

$(document).ready(function(e){
    /*$("body").smoothWheel()*/

    //code for display price slider in homepage
    function homepage_search(){
        var wi = $(window).width();
        if (wi <= 480){
            $("div").removeClass("form-login").removeClass("col-md-8").removeClass("col-md-offset-2").removeClass("line_set");
        }
        if (wi <= 768){
            $("div").removeClass("line_set");
        }
        //popup banner when homepage load
        /*  $('#popmodal').modal('show');*/

        //set price on the slider dynamically
        odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {
            //code for sale.............................................
            $(".form_filter_sale .home_page_filter_price #amount").val("$" + 0 + " - $" + data['max_value']);
//            $('#min_property_range_id').val(0);
//            $('#max_property_range_id').val(data['max_value']);
            $('.form_filter_sale .home_page_filter_price #min_property_range_id').val(0);
            $('.form_filter_sale .home_page_filter_price #max_property_range_id').val(data['max_value']);
            $(".form_filter_sale .home_page_filter_price #slider_range").slider({
                range: true,
                animate: true,
                step: 500,
                min: 0,
                max: data['max_value'],
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                scale: [0, '|', 50, '|', '100', '|', 250, '|', 500],
                values: [data['min_value'], data['max_value']],
                slide: function(event, ui) {
                    $(".form_filter_sale .home_page_filter_price #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
//                $(".home_page_filter_price #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);

//                    $(".home_page_filter_price  #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
//                    $('#min_property_range_id').val(ui.values[0]);
//                    $('#max_property_range_id').val(ui.values[1]);

                    $(".form_filter_sale .home_page_filter_price #min_property_range_id").val(ui.values[0]);
                    $(".form_filter_sale .home_page_filter_price #max_property_range_id").val(ui.values[1]);

//                    $('.home_page_filter_price #min_property_range_id').val(ui.values[0]);
//                    $('.home_page_filter_price #max_property_range_id').val(ui.values[1]);
                }
            });
//            $("#amount").val("$" + $("#slider_range").slider("values", 0) + " - $" + $("#slider_range").slider("values", 1));
//            var $amount = $("#amount").val();
//            $('#slider_range a').first().html('<label><span class="glyphicon glyphicon-chevron-left"></span></label>');
//            $('#slider_range a').first().next().html('<label><span class="glyphicon glyphicon-chevron-right"></span></label>');

            $(".form_filter_sale .home_page_filter_price #amount").val("$" + $(".home_page_filter_price #slider_range").slider("values", 0) + " - $" + $(".home_page_filter_price #slider_range").slider("values", 1));
            var $amount = $(".form_filter_sale .home_page_filter_price #amount").val();
            $('.form_filter_sale .home_page_filter_price #slider_range span').html('<label><span class="fa fa-chevron-left"></span></label>');
            $('.form_filter_sale .home_page_filter_price #slider_range span').next().html('<label><span class="fa fa-chevron-right"></span></label>');

            //code for rent.............................................
            $(".form_filter_rent .home_page_filter_price #amount").val("$" + 0 + " - $" + data['max_value']);
//            $('#min_property_range_id').val(0);
//            $('#max_property_range_id').val(data['max_value']);
            $('.form_filter_rent .home_page_filter_price #min_property_range_id').val(0);
            $('.form_filter_rent .home_page_filter_price #max_property_range_id').val(data['max_value']);
            $(".form_filter_rent .home_page_filter_price #slider_range").slider({
                range: true,
                animate: true,
                step: 500,
                min: 0,
                max: data['max_value'],
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                scale: [0, '|', 50, '|', '100', '|', 250, '|', 500],
                values: [data['min_value'], data['max_value']],
                slide: function(event, ui) {
                    $(".form_filter_rent .home_page_filter_price #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
//                $(".home_page_filter_price #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
//                    $(".home_page_filter_price  #amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
//                    $('#min_property_range_id').val(ui.values[0]);
//                    $('#max_property_range_id').val(ui.values[1]);
                    $(".form_filter_rent .home_page_filter_price #min_property_range_id").val(ui.values[0]);
                    $(".form_filter_rent .home_page_filter_price #max_property_range_id").val(ui.values[1]);

//                    $('.home_page_filter_price #min_property_range_id').val(ui.values[0]);
//                    $('.home_page_filter_price #max_property_range_id').val(ui.values[1]);
                }
            });
//            $("#amount").val("$" + $("#slider_range").slider("values", 0) + " - $" + $("#slider_range").slider("values", 1));
//            var $amount = $("#amount").val();
//            $('#slider_range a').first().html('<label><span class="glyphicon glyphicon-chevron-left"></span></label>');
//            $('#slider_range a').first().next().html('<label><span class="glyphicon glyphicon-chevron-right"></span></label>');

            $(".form_filter_rent .home_page_filter_price #amount").val("$" + $(".form_filter_rent .home_page_filter_price #slider_range").slider("values", 0) + " - $" + $(".form_filter_rent .home_page_filter_price #slider_range").slider("values", 1));
            var $amount = $(".form_filter_rent .home_page_filter_price #amount").val();
            $('.form_filter_rent .home_page_filter_price #slider_range a').html('<label><span class="glyphicon glyphicon-chevron-left"></span></label>');
            $('.form_filter_rent .home_page_filter_price #slider_range a').next().html('<label><span class="glyphicon glyphicon-chevron-right"></span></label>');
        });

        // bedroom slide js
        $("#bead_slider_range").slider({
            range: true,
            animate: true,
            step: 1,
            min: 1,
            max: 5,
            heterogeneity: ['50/50000'],
            format: {
                format: '##.0',
                locale: 'de'
            },
            dimension: '',
            values: [$('#min_bead_range_id').val(), $('#max_bead_range_id').val()],
            slide: function(event, ui) {
                $("#bead_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                $('#min_bead_range_id').val(ui.values[0]);
                $('#max_bead_range_id').val(ui.values[1]);
            }
        });
        $("#bead_amount").val("" + $("#bead_slider_range").slider("values", 0) + " - " + $("#bead_slider_range").slider("values", 1));
        var $bead_amount = $("#bead_amount").val();
        $('#bead_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
        $('#bead_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

        //  bathroom slide js
        $("#bath_slider_range").slider({
            range: true,
            animate: true,
            step: 1,
            min: 1,
            max: 5,
            heterogeneity: ['50/50000'],
            format: {
                format: '##.0',
                locale: 'de'
            },
            dimension: '',
            values: [$('#min_bath_range_id').val(), $('#max_bath_range_id').val()],
            slide: function(event, ui) {
                $("#bath_amount").val("" + ui.values[0] + "-" + ui.values[1]);
                $('#min_bath_range_id').val(ui.values[0]);
                $('#max_bath_range_id').val(ui.values[1]);
            }
        });
        $("#bath_amount").val("" + $("#bath_slider_range").slider("values", 0) + " - " + $("#bath_slider_range").slider("values", 1));
        var $bath_amount = $("#bath_amount").val();
        $('#bath_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
        $('#bath_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');

        // Price list slide js
//        odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {
//            $("#price_slider_range").slider({
//                range: true,
//                animate: true,
//                step: 500,
//                min: data['min_value'],
//                max: data['max_value'],
//                heterogeneity: ['50/50000'],
//                format: {
//                    format: '##.0',
//                    locale: 'de'
//                },
//                dimension: '',
//                values: [$('#min_price_range_id').val(), $('#max_price_range_id').val()],
//                slide: function(event, ui) {
//                    $("#price_slider").val("$" + ui.values[0] + "- $" + ui.values[1]);
//                    $('#min_price_range_id').val(ui.values[0]);
//                    $('#max_price_range_id').val(ui.values[1]);
//                }
//            });
////            $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));
//
//            $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));
//
////            $("#min_range").val(data['min_value'])
////            $("#max_range").val(data['max_value'])
//            $(".min_range_class").val(data['min_value'])
//            $(".max_range_class").val(data['max_value'])
//
//            var $price_slider = $("#price_slider").val();
//
//            $('#price_slider_range a').first().html('<label><span class="glyphicon glyphicon-chevron-left"></span></label>');
//            $('#price_slider_range a').first().next().html('<label><span class="glyphicon glyphicon-chevron-right"></span></label>');
//        });

         odoo.jsonRpc("/min_max_price", 'call', {}).then(function(data) {
            $("#price_slider_range").slider({
                range: true,
                animate: true,
                step: 500,
                min: data['min_value'],
                max: data['max_value'],
                heterogeneity: ['50/50000'],
                format: {
                    format: '##.0',
                    locale: 'de'
                },
                dimension: '',
                values: [$('#min_price_range_id').val(), $('#max_price_range_id').val()],
                slide: function(event, ui) {
                    $("#price_slider").val("$" + ui.values[0] + "- $" + ui.values[1]);
                    $('#min_price_range_id').val(ui.values[0]);
                    $('#max_price_range_id').val(ui.values[1]);
                }
            });
//            $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));

            $("#price_slider").val("$" + $("#price_slider_range").slider("values", 0) + " - $" + $("#price_slider_range").slider("values", 1));

//            $("#min_range").val(data['min_value'])
//            $("#max_range").val(data['max_value'])
            $(".min_range_class").val(data['min_value'])
            $(".max_range_class").val(data['max_value'])

            var $price_slider = $("#price_slider").val();

            $('#price_slider_range span').first().html('<label><span class="fa fa-chevron-left"></span></label>');
            $('#price_slider_range span').first().next().html('<label><span class="fa fa-chevron-right"></span></label>');
        });
    }

    //code for homepage content
    function homepage(){
        document.title = 'Homepage';
        window.history.pushState("Homepage", "Homepage", "/");
        odoo.jsonRpc("/homepage", 'call', {}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/"]').parent().addClass('active');
                homepage_search();
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '.navbar-default a', function(e){
        $(this).each( function() {
            $(this).parent().removeClass('active');
        });
        $(this).parent().addClass('active');
    })

    $(document).on('click', 'a[href="/"]', function(e){
        e.preventDefault();
        homepage()
    })

    //code for click on navbar in responsive view
    $(document).on('click', '.nav.sidebar-nav li .is-closed', function(e){
        if (this['id'] == 'user_account_logout'){
            $(document).find("ul.nav.sidebar-nav li a").addClass('is-open');
        }
        if (this['id'] != 'user_account_logout'){
            $('.hidden-md.hidden-lg.toggled ul.nav.sidebar-nav li a').removeClass('active');
            $(document).find("#wrapper").removeClass('toggled');
            $('#wrapper .overlay').css('display', 'none');
        }
    });
    $(document).on('click', '.nav.sidebar-nav li .is-open', function(e){
        if (this['id'] =='user_account_logout'){
            $(document).find("ul.nav.sidebar-nav li a").addClass('is-open');
        }
        if (this['id'] !='user_account_logout'){
            $('.hidden-md.hidden-lg.toggled ul.nav.sidebar-nav li a').removeClass('active');
            $(document).find("#wrapper").removeClass('toggled');
            $('#wrapper .overlay').css('display', 'none');
        }
    });

    //code for buypage content
    function buypage(){
        document.title = 'Buy';
        if (window.location.pathname != '/buy'){
            window.history.pushState("Buy Properties", "Buy", "/buy");
        }
        odoo.jsonRpc("/buy_properties", 'call', {}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/buy"]').parent().addClass('active');
            });
            $(window).scrollTop(0);
        });
    }
    $(document).on('click', 'a[href="/buy"]', function(e){
        e.preventDefault();
//        buypage()
        allassetsalepage()
    })
    $(document).on('click', 'a[href="/rent"]', function(e){
        e.preventDefault();
//        buypage()
        allassetleasepage()
    })

    //code for sales page content
    function salespage(){
        document.title = 'Sales';
        if (window.location.pathname != '/sell'){
            window.history.pushState("Sell Properties", "Sales", "/sell");
        }
        odoo.jsonRpc("/sell_properties", 'call', {}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/sell"]').parent().addClass('active');
            });
            $(window).scrollTop(0);
        });
    }
    $(document).on('click', 'a[href="/sell"]', function(e){
        e.preventDefault();
        salespage()
    });

    function mypropertypage(){
        document.title = 'My Properties';
        if (window.location.pathname != '/my_properties'){
            window.history.pushState("My Properties", "Properties", "/my_properties");
        }
        odoo.jsonRpc("/my_properties_json", 'call', {}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/my_properties"]').parent().addClass('active');
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', 'a[href="/my_properties"]', function(e){
        e.preventDefault();
        mypropertypage()
    });

    //code for scroll in all page and display navbar smoothly transparent to white
    $(document).scroll(function() {
        var dHeight = $(this).height() - ($('.feature-properties').height());
        if (dHeight >= $(this).scrollTop() - 500) {
            $('.navbar-default').css('background', 'rgba(255,255,255,' + $(this).scrollTop() / dHeight + ')');
        }
    });
    $(window).bind('scroll', function () {
        if ($(window).scrollTop() > 50) {
            $("#wrapwrap").find(".navbar-static-top.navbar-fixed-top").css('top', 0);
            if ($('nav#oe_main_menu_navbar').length){
                $("nav#oe_main_menu_navbar").css('display', 'none');
                $("#wrapwrap").find('main').addClass('with-navbar');
            }

        } else {
            $("#wrapwrap").find(".navbar-static-top.navbar-fixed-top").css('top', 'inherit');
            if ($('nav#oe_main_menu_navbar').length){
                $("nav#oe_main_menu_navbar").css('display', 'block');
                $("#wrapwrap").find('main').removeClass('with-navbar');
            }
        }
    });


    $(document).on('click', '.hero-text', function(e){
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $('.rest').offset().top - 50
        }, 1000);
        
    });

    //code for advance search "link" in all page
     /*$('#advance_search').click(function(){
        odoo.jsonRpc("/advance_search", 'call', {}).then(function(modal) {
            $(modal).appendTo($('body'))
            .modal()
            .on('hidden.bs.modal', function () {
                $(this).remove();
            });
        });
    })*/

//    var sourceSwap = function () {
//        var $this = $(this);
//        var newSource = $this.data('alt-src');
//        $this.data('alt-src', $this.attr('src'));
//        $this.fadeOut(250, function() {
//            $this.attr('src', newSource)
//        }).fadeIn(250);
//    }
//
//    $(document).on('hover', '.property-images img.img-responsive#property_image11', sourceSwap)

//    $(document).on('hover', '.property-images img.img-responsive', sourceSwap, sourceSwap)

    // code for contactus page
    function contactuspage(){
        document.title = 'Contact us';
//        alert(window.location.pathname)
        if (window.location.pathname != '/contactus'){
            window.history.pushState("Contact us", "Contact us", "/contactus");
        }
        odoo.jsonRpc("/contactus_display", 'call', {}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/page/contactus"]').parent().addClass('active');
                function initMap() {
                    if (typeof google !== 'undefined') {
                        var latitude = 0
                        var longitude = 0
                        odoo.jsonRpc("/company_detail", 'call', {}).then(function(data) {

                            //var add= data.street + ' '+  data.city +' ' +  data.country
                            ////var add=data.street + ' ' + data.street2 + ' ' + data.city + ' ' + data.state + ' ' + data.country + ' ' + data.zip;
                            //var geocoder =  new google.maps.Geocoder();
                            //$(document).find('#contacts-map').attr('src', 'https://maps.google.co.in/maps?f=q&source=s_q&hl=en&geocode=&q=' + add+'&t=m&z=14&ll=' + data.latitude_data + ',' + data.longitide_data + '&output=embed');

                            var map = new google.maps.Map(document.getElementById('contacts-map'), {
                              zoom: 16,
                              center: {lat: data.latitude_data, lng: data.longitide_data}
                              //center: {lat: 23, lng: 72}
                            });
                            var image = {
                              size: new google.maps.Size(60, 70),
                              origin: new google.maps.Point(0, 0),
                              anchor: new google.maps.Point(35, 70)
                            };
                            var marker = new google.maps.Marker({
                              position: {lat: data.latitude_data, lng: data.longitide_data},
                              map: map,
                              icon: image
                            });
                            google.maps.event.addListener(map, 'zoom_changed', function () {
                              map.setCenter(marker.getPosition());
                            });
                            google.maps.event.addDomListener(window, 'resize', function () {
                              map.setCenter(marker.getPosition());
                            });
                        });
                        if( $(document).find("#oe_main_menu_navbar").length )         // use this if you are using id to check
                        {
                            $(document).find(".hero-section").addClass('with_nav_hero_section');
                            $("#wrapwrap").css('height', 'initial');
                        }
                    }
                  }
                  initMap();
            });
        });

    }
 if( $('div').css('position') == 'absolute' && $('div').css('left') == '0px' && $('div').css('top') == '0px')  {
        alert('1')
    }

    // code for create new lead in contact us page
    $(document).on('click', '#button_send', function(e){
        $('#contactForm').validator('validate');
        if ($('#contactForm').find('.has-error:visible').size() > 0) return;
        odoo.jsonRpc("/contactus/create_lead", 'call', {
            'contact_name' : $("input[name='contact_name']").val(),
            'phone' : $("input[name='phone']").val(),
            'email_from' : $("input[name='email_from']").val(),
            'partner_name' : $("input[name='partner_name']").val(),
            'name' : $("input[name='name']").val(),
            'description' : $("textarea[name='description']").val(),
            'value_from' :"Contactus page",
        }).then(function() {
            $('#contactForm')[0].reset();
            $("#display_success_msg").css('display', 'block');
        });
    });
    $(document).on('click', 'a[href="/page/contactus"]', function(e){
        e.preventDefault();
        contactuspage()
    });
    if (window.location.pathname == '/contactus'){
        contactuspage()
    }
    $(document).on('click', 'a[href="/contactus"]', function(e){
        e.preventDefault();
        contactuspage()
    });

// create lead from sales page
    $(document).on('click', '#submit_sale_form', function(e){
        $('#saleForm').validator('validate');
        if ($('#saleForm').find('.has-error:visible').size() > 0) return;
        odoo.jsonRpc("/contactus/create_lead", 'call', {
            'contact_name' : $("input[name='first_name']").val() +' '+$("input[name='last_name']").val(),
            'phone' : $("input[name='phone']").val(),
            'email_from' : $("input[name='email_from']").val(),
            'address' : $("input[name='address']").val(),
            'city' : $("input[name='city']").val(),
            'zip' : $("input[name='zip']").val(),
            'country_id' : $("select[name='country_id']").val(),
            'value_from' : "Sales page",
        }).then(function() {
            $('#saleForm')[0].reset();
            $("#display_success_msg").css('display', 'block');
        });
    });

// create lead from perticular property page
    $(document).on('click', '#send_property_id', function(e){
        $('#selectedpropertyForm').validator('validate');
        if ($('#selectedpropertyForm').find('.has-error:visible').size() > 0) return;
        odoo.jsonRpc("/contactus/create_lead", 'call', {
            'contact_name' : $("input[name='first_name']").val() +' '+ $("input[name='last_name']").val(),
            'phone' : $("input[name='phone']").val(),
            'email_from' : $("input[name='email_from']").val(),
            'telType' : $("select[name='telType']").val(),
            'telTime' : $("select[name='telTime']").val(),
            'msg' : $("textarea[name='msg']").val(),
            'asset': $("input[name='asset']").val(),
            'value_from' : "Property page",
        }).then(function() {
            $('#selectedpropertyForm')[0].reset();
            $("#display_success_msg").css('display', 'block');
        });
    });

// code for back and forward button in browser
    if (window.history && window.history.pushState) {
        $(window).on('popstate', function() {
            if (window.location.pathname == '/' || window.location.pathname == '/page/homepage'){
                document.title = 'Homepage';
//                window.history.pushState("Homepage", "Homepage", "/");
                odoo.jsonRpc("/homepage", 'call', {}).then(function(data) {
                    $('main').fadeOut("slow", function() {
                        $('main').html(data).fadeIn("slow");
                        $('.navbar-default a').parent().removeClass('active');
                        $('.navbar-default a[href="/"]').parent().addClass('active');
                        homepage_search()
                    });
                    $(window).scrollTop(0);
                });
            }
            if (window.location.pathname == '/contactus'){
                 contactuspage()
            }
            if (window.location.pathname == '/sell'){
                salespage()
            }
            if (window.location.pathname == '/buy'){
//                buypage()
                allassetsalepage()
            }
            if (window.location.pathname == '/all_asset_lease'){
                allassetleasepage()
            }
            if (window.location.pathname == '/all_asset_sale'){
                allassetsalepage()
            }
            if (window.location.pathname == '/all_past_sale'){
                allassetpastsalepage()
            }
            if (window.location.pathname == '/saved_sell'){
                allassetsavedsalepage()
            }
            if (window.location.pathname == '/my_properties'){
                mypropertypage()
            }
            if (window.location.pathname == '/all_past_lease'){
                allassetpastleasepage()
            }
            if (window.location.pathname == '/selected_property_page'){
                var sPageURL = window.location.search.substring(1);
                var ca = sPageURL.split('=');
                var selected_property_id = ca[1]
                    odoo.jsonRpc("/selected_property", 'call', {
                    'selected_property_id' : selected_property_id,
                }).then(function(data) {
                    $('main').fadeOut("slow", function() {
                        $('main').html(data).fadeIn("slow");
    //                    displayTotalCookieProducts()
                        $('.navbar-default a').parent().removeClass('active');
                        $('.navbar-default a[href="/buy"]').parent().addClass('active');
                        suggested_property_flex_slider()
                    });
                    $(window).scrollTop(0);
                });
            }
        });
    }

    var x = document.cookie;
//    function for get total property ids from cookie
    function getCookie1(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
        }
        return "";
    }

    //code for display total favorite product in cookie and total favorite products of logged user
    function set_id_in_saved_page(){
        if (window.location.pathname == '/saved_sell'){
            var property_type = window.sessionStorage.getItem('display_type')
            var id = ""
            if (property_type == 'alllease'){
                id = 'view_all_asset_lease'
            }
            if (property_type == 'allsales'){
                id = 'view_all_asset_sale'
            }
            if (property_type == 'allpastsale'){
                id = 'view_all_past_sales'
            }
            if (property_type == 'allpastlease'){
                id = 'view_all_past_lease'
            }
            $('#allassetsavedproperty_section #display_saved_properties .navbar-nav li a.sales_type').attr('id', id);
        }
    }
    function displayTotalCookieProducts(){
        var html_content = $('html')
        var website_user_id = html_content.data('website_user_id');
        var logged_user_id = html_content.data('user_id');
        if(website_user_id == logged_user_id){
            var all_property_cookies_ids = getCookie1("property_id");
            var arr = all_property_cookies_ids.split(',');
            if (arr.indexOf('') != -1){
                arr.splice(arr.indexOf(''),1);
            }
            var total_properties = arr.length;
            var display_saved = 'Saved (' + total_properties +')'
            set_id_in_saved_page()
            $("#view_all_asset_sale_saved").html(display_saved)
            $("#view_all_asset_sale_saved").attr('style', 'width: 105px');
        }
        if(website_user_id != logged_user_id){
            var $this = $(this);
            odoo.jsonRpc("/search_total_fav_property_when_looged_in", 'call', {
            }).then(function(total_fav_property) {
                var total_properties = total_fav_property;
                var display_saved = 'Saved (' + total_properties +')'
                set_id_in_saved_page()
                $("#view_all_asset_sale_saved").html(display_saved)
                $("#view_all_asset_sale_saved").attr('style', 'width: 105px');
            });
        }
    }
    displayTotalCookieProducts()

//    code for render lease page
    function allassetleasepage(value){
        document.title = 'All Lease';
        if (window.location.pathname != '/all_asset_lease'){
            window.history.pushState("All Lease", "All Lease", "/all_asset_lease");
        }
        if (value === undefined) {
            value = {}
        }
        var sPageURL = window.location.search.substring(1);
        var ca = sPageURL.split('=');
        var page = ca[1]
        value['page'] = page
        odoo.jsonRpc("/allassetlease_display", 'call', value).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                displayTotalCookieProducts()
                var property_type = $("#property_type").val();
                window.sessionStorage.setItem('display_type', property_type);
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/rent"]').parent().addClass('active');
                homepage_search();
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '#view_all_asset_lease', function(e){
        allassetleasepage()
    });

//    code for render all sales page
    function allassetsalepage(value){
        document.title = 'All Sales';
        if (window.location.pathname != '/all_asset_sale'){
            window.history.pushState("All Sales", "All Sales", "/all_asset_sale");
        }
        if (value === undefined) {
            value = {}
        }
        var sPageURL = window.location.search.substring(1);
        var ca = sPageURL.split('=');
        var page = ca[1]
        value['page'] = page

        odoo.jsonRpc("/allassetsale_display", 'call', value).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                displayTotalCookieProducts()
                var property_type = $("#property_type").val();
                window.sessionStorage.setItem('display_type', property_type);
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/buy"]').parent().addClass('active');
                homepage_search();
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '#view_all_asset_sale', function(e){
        allassetsalepage()
    });

//    code for render past sales page
    function allassetpastsalepage(value){
        document.title = 'All Past Sales';
        if (window.location.pathname != '/all_past_sale'){
            window.history.pushState("All Past Sales", "All Past Sales", "/all_past_sale");
        }
        if (value === undefined) {
            value = {}
        }
        var sPageURL = window.location.search.substring(1);
        var ca = sPageURL.split('=');
        var page = ca[1]
        value['page'] = page
        odoo.jsonRpc("/allassetpastsale_display", 'call', value).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                displayTotalCookieProducts()
                var property_type = $("#property_type").val();
                window.sessionStorage.setItem('display_type', property_type);
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/buy"]').parent().addClass('active');
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '#view_all_past_sales', function(e){
        allassetpastsalepage()
    });

    //code for render past lease page
    function allassetpastleasepage(value){
        document.title = 'All Past Lease';
        if (window.location.pathname != '/all_past_lease'){
            window.history.pushState("All Past Lease", "All Past Lease", "/all_past_lease");
        }
        if (value === undefined) {
            value = {}
        }
        var sPageURL = window.location.search.substring(1);
        var ca = sPageURL.split('=');
        var page = ca[1]
        value['page'] = page
        odoo.jsonRpc("/allassetpastlease_display", 'call', value).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                displayTotalCookieProducts()
                var property_type = $("#property_type").val();
                window.sessionStorage.setItem('display_type', property_type);
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/rent"]').parent().addClass('active');
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '#view_all_past_lease', function(e){
        allassetpastleasepage()
    });

// code for click "Buy" on home page
    $(document).on('click', '#sale_btn_id', function(e){
        var $this = $(this);
        var form_filter_class = $(this).parent().parent('form.form_filter_sale');
        var total_selected_property_type_ids = [];
//        $('#check_property:checked').each(function(){
        form_filter_class.find('#check_property:checked').each(function(){
             var selected_id =$(this).data('property_type_id')
             total_selected_property_type_ids.push(selected_id);
        });

//        var min_range = form_filter_class.find('input#min_range').val();
//        var max_range = form_filter_class.find('input#max_range').val();
//        if (max_range <= min_range){
//            alert('Maximum range should be greater than Minimum range');
//            return false
//        }

        window.history.pushState("All Sales", "All Sales", "/all_asset_sale");
        odoo.jsonRpc("/allassetsale_display", 'call', {
            'postcode' : form_filter_class.find('input.postal_code').val(),
            'area' : form_filter_class.find('input.street_name').val(),
            'city' : form_filter_class.find('input.locality').val(),
            'state' : form_filter_class.find('input.administrative_area_level_1').val(),
            'country' : form_filter_class.find('input.country').val(),
            'min_range': form_filter_class.find('input#min_property_range_id').val(),
            'max_range': form_filter_class.find('input#max_property_range_id').val(),
            'click_value': $this.data('click_value'),
            'total_selected_property_type_ids':total_selected_property_type_ids,
        }).then(function(data) {
        $('main').fadeOut("slow", function() {
            $('main').html(data).fadeIn("slow");
            displayTotalCookieProducts()
            var property_type = $("#property_type").val();
            window.sessionStorage.setItem('display_type', property_type);
            $('.navbar-default a').parent().removeClass('active');
            $('.navbar-default a[href="/buy"]').parent().addClass('active');
            homepage_search();
        });
        $(window).scrollTop(0);
        });
    });

// code for click "Rent" on home page
    $(document).on('click', '#rent_btn_id', function(e){
        var $this = $(this);
        var form_filter_class = $(this).parent().parent('form.form_filter_rent');
        var total_selected_property_type_ids = [];
//        $('#check_property:checked').each(function(){
        form_filter_class.find('#check_property:checked').each(function(){
             var selected_id =$(this).data('property_type_id')
             total_selected_property_type_ids.push(selected_id);
        });
        window.history.pushState("All Lease", "All Lease", "/all_asset_lease");
        odoo.jsonRpc("/allassetlease_display", 'call',{
            'postcode' : form_filter_class.find('input.postal_code').val(),
            'area' : form_filter_class.find('input.street_name').val(),
            'city' : form_filter_class.find('input.locality').val(),
            'state' : form_filter_class.find('input.administrative_area_level_1').val(),
            'country' : form_filter_class.find('input.country').val(),
            'min_range': form_filter_class.find('input#min_property_range_id').val(),
            'max_range': form_filter_class.find('input#max_property_range_id').val(),
            'click_value': $this.data('click_value'),
            'total_selected_property_type_ids': total_selected_property_type_ids,
        }).then(function(data) {
        $('main').fadeOut("slow", function() {
            $('main').html(data).fadeIn("slow");
            displayTotalCookieProducts()
            var property_type = $("#property_type").val();
            window.sessionStorage.setItem('display_type', property_type);
            $('.navbar-default a').parent().removeClass('active');
            $('.navbar-default a[href="/rent"]').parent().addClass('active');
            homepage_search();
        });
        $(window).scrollTop(0);
        });
    });

    //code for filter property on all pages
    function search_properties_lease_sale_page(value){
        var property_type = $("#property_type").val();
        if (value === undefined) {
            value = {}
        }
        var $this = $(this);
        var total_selected_property_type_ids = [];
        $('#check_property:checked').each(function(){
             var selected_id =$(this).data('property_type_id')
             total_selected_property_type_ids.push(selected_id);
        });
        value['postcode'] = $("input[name='postcode']").val();
        value['area'] = $("input[name='area']").val();
        value['city'] = $("input[name='city']").val();
        value['min_range'] = $("input[name='min_range']").val();
        value['max_range'] = $("input[name='max_range']").val();
        value['min_bath'] = $("input[name='min_bath']").val();
        value['max_bath'] = $("input[name='max_bath']").val();
        value['min_bead'] = $("input[name='min_bead']").val();
        value['max_bead'] = $("input[name='max_bead']").val();
        value['dropdown_furnish'] = $("select[name='dropdown_furnish']").val();
        value['dropdown_facing'] = $("select[name='dropdown_facing']").val();
        value['dropdown_price'] = $("select[name='dropdown_price']").val();
        value['total_selected_property_type_ids'] = total_selected_property_type_ids
        if (property_type == 'allsales'){
            value['click_value'] = 'buy'
            allassetsalepage(value)
        }
        if (property_type == 'alllease'){
            value['click_value'] = 'rent'
            allassetleasepage(value)
        }
    }

    $(document).on('slidestop', '#bath_slider_range', function(e){
       search_properties_lease_sale_page();
    });

    $(document).on('slidestop', '#price_slider_range', function(e){
       search_properties_lease_sale_page();
    });
    $(document).on('slidestop', '#bead_slider_range', function(e){
       search_properties_lease_sale_page();
    });

    $(document).on('change', '.dropdown.open', function(e){
       search_properties_lease_sale_page();
    });

    $(document).on('click', '.dropdown-menu', function(e){
        e.stopPropagation();
    });

    // Add slideDown animation to dropdown
    /*$('.dropdown').on('show.bs.dropdown', function(e){
    //$(document).on('click', '.dropdown', function(e){
      $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });

    // Add slideUp animation to dropdown
    $('.dropdown').on('hide.bs.dropdown', function(e){
      $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });*/

//    code for select heart image then add value of property in cookie
    $(document).on('click', '.listing-save', function(e){
//        alert(request.website.user_id.id)
        var html_content = $('html')
        var website_user_id = html_content.data('website_user_id');
        var logged_user_id = html_content.data('user_id');
        if(website_user_id == logged_user_id){
            var list = []
            function getCookie(cname) {
                var name = cname + "=";
                var ca = document.cookie.split(';');
                for(var i=0; i<ca.length; i++) {
                    var c = ca[i];
                    while (c.charAt(0)==' ') c = c.substring(1);
                    if (c.indexOf(name) == 0)
                    {
                        list.push(c.substring(name.length, c.length));
                    }
                }
                return "";
            }
            var product_id = getCookie("property_id");

            var $this = $(this);
            var lease_id = $this.data('lease_id');

            function setCookie(cname, cvalue, exdays) {
                var name = cname + "=";
                var d = new Date();
                d.setTime(d.getTime() + (exdays*24*60*60*1000));
                var expires = "expires="+d.toUTCString();
                list.push(cvalue);
                document.cookie = cname + "=" + list + "; " + expires;
            }
            var create_cookie = setCookie("property_id", lease_id, 365);

            displayTotalCookieProducts()

            var $this = $(this);
            var parent_div =$(this).parent()
            var second_img = jQuery(parent_div).children(".listing-saved-data");

            var display_heart_hover = jQuery(parent_div).children("#display_heart_hover");
            display_heart_hover.css('display', 'block');

            second_img.data('check_value', 'true');

            $(this).attr('style', 'display: none');
           /* $(second_img).attr('style', 'display:block');*/
            /*$(second_img).attr('style', 'margin-top:-5%;');*/
            $(second_img).attr('style', 'display:block;cursor:pointer;');
        }

        if(website_user_id != logged_user_id){
            var $this = $(this);
            var lease_id = $this.data('lease_id');
            odoo.jsonRpc("/change_fav_property", 'call', {
                'fav_checked': 'True',
                'fav_property': lease_id
            }).then(function(data) {
                displayTotalCookieProducts()
                var parent_div =$this.parent()
                var second_img = jQuery(parent_div).children(".listing-saved-data");

                var display_heart_hover = jQuery(parent_div).children("#display_heart_hover");
                display_heart_hover.css('display', 'block');

                second_img.data('check_value', 'true');

                $this.attr('style', 'display: none');
                $(second_img).attr('style', 'display:block;cursor:pointer;');

            });
        }
    });

    // code for click on pagination
    $(document).on('click', '.products_pager ul li a', function(e){
        e.preventDefault();
        var property_type = $("#property_type").val();
        window.sessionStorage.setItem('display_type', property_type);
        var view = {}
        view['property_type'] = property_type
        if ($(this).text() == '»'){
//        if ($(this).text() == 'Next'){
            view['page'] = parseInt($('.products_pager ul li.active a')[0].text) + 1;
//        }else if($(this).text() == 'Prev'){
        }else if($(this).text() == '«'){
            view['page'] = parseInt($('.products_pager ul li.active a')[0].text) - 1;
        }else{
            view['page'] = $(this).text();
        }

        if (window.location.pathname == '/all_asset_lease'){
            window.history.pushState("All Lease", "All Lease", "/all_asset_lease"+"?"+"page="+view['page']);
            search_properties_lease_sale_page(view)
        }
        if (window.location.pathname == '/all_asset_sale'){
            window.history.pushState("All Sales", "All Sales", "/all_asset_sale"+"?"+"page="+view['page']);
            search_properties_lease_sale_page(view)
        }
        if (window.location.pathname == '/all_past_sale'){
            window.history.pushState("All Past Sales", "All Past Sales", "/all_past_sale"+"?"+"page="+view['page']);
            allassetpastsalepage(view)
        }
        if (window.location.pathname == '/all_past_lease'){
            window.history.pushState("All Past Lease", "All Past Lease", "/all_past_lease"+"?"+"page="+view['page']);
            allassetpastleasepage(view)
        }
    });

    //code for selected property
     function selected_property_json_call(selected_property_id){
        document.title = 'Property';
        window.history.pushState("Selected Property", "Property", "/selected_property_page" + "?"+"id="+selected_property_id);
        odoo.jsonRpc("/selected_property", 'call', {'selected_property_id' : selected_property_id}).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                $('.navbar-default a').parent().removeClass('active');
                $('.navbar-default a[href="/buy"]').parent().addClass('active');
                setInterval(function(){ suggested_property_flex_slider() }, 500);
            });
            $(window).scrollTop(0);
        });
     }

     function suggested_property_flex_slider(){
    	 if ($('.flexslider')){
    		 $('.flexslider').flexslider({
	            animation: "slide",
	            animationLoop: false,
	            itemWidth: 385,
	            /*itemWidth: 300,*/
	            itemMargin: 5
	          });
    	 }
          
     }
    $(window).load(function() {
        if (window.location.pathname == '/selected_property_page'){
            suggested_property_flex_slider()
        }
        if (window.location.pathname == '/' || window.location.pathname == '/page/homepage' || window.location.pathname == '/all_asset_lease' || window.location.pathname == '/all_asset_sale'){
            homepage_search()
        }
        if (window.location.pathname == '/all_asset_sale'){
            homepage_search()
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.navbar-default a[href="/buy"]').parent().addClass('active');
        }
        if (window.location.pathname == '/all_asset_lease'){
            homepage_search()
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.navbar-default a[href="/rent"]').parent().addClass('active');
        }
        if (window.location.pathname == '/saved_sell'){
            var property_type = window.sessionStorage.getItem('display_type')
            if (property_type == 'alllease'){
                $('.nav.sidebar-nav li a').removeClass('active');
                $('.navbar-default a[href="/rent"]').parent().addClass('active');
            }
            if (property_type == 'allsales'){
                $('.nav.sidebar-nav li a').removeClass('active');
                $('.navbar-default a[href="/buy"]').parent().addClass('active');
            }
        }
    });
     //code for click on property name then redirect property page
     $(document).on('click', '.property_name', function(e){
        var $this = $(this);
        var selected_property_id = parseInt($this.data('lease_id'));
        selected_property_json_call(selected_property_id)
     });

    //code for click on property image then redirect property page
     $(document).on('click', '#property_image11', function(e){
        var $this = $(this);
        var selected_property_id= parseInt($this.parent().children().children('.property_name').data('lease_id'));
        selected_property_json_call(selected_property_id)
     });

    //code for click on property image then redirect property page
     $(document).on('click', '#img_hover', function(e){
        var $this = $(this);
        var selected_property_id= parseInt($this.parent().children().children('.property_name').data('lease_id'));
        selected_property_json_call(selected_property_id)
     });

    //code for saved properties on sales page
    function allassetsavedsalepage(){
        var property_type = window.sessionStorage.getItem('display_type')
        document.title = 'Saved Sales';
        if (window.location.pathname != '/saved_sell'){
            window.history.pushState("Saved Sell Properties", "Sales", "/saved_sell");
        }
        odoo.jsonRpc("/saved_sell_properties_display", 'call', {
                'property_type':property_type
        }).then(function(data) {
            $('main').fadeOut("slow", function() {
                $('main').html(data).fadeIn("slow");
                displayTotalCookieProducts()
                $('.navbar-default a').parent().removeClass('active');
                if (property_type == 'alllease'){
                    $('.nav.sidebar-nav li a').removeClass('active');
                    $('.navbar-default a[href="/rent"]').parent().addClass('active');
                }
                if (property_type == 'allsales'){
                    $('.nav.sidebar-nav li a').removeClass('active');
                    $('.navbar-default a[href="/buy"]').parent().addClass('active');
                }
            });
            $(window).scrollTop(0);
        });
    }

    $(document).on('click', '#view_all_asset_sale_saved', function(e){
        allassetsavedsalepage()
    });

    $(document).on('click', '.hamburger.is-open', function(e){
        if (window.location.pathname == '/' || window.location.pathname == '/page/homepage'){
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.nav.sidebar-nav li a[href="/"]').addClass('active');
        }
        if (window.location.pathname == '/contactus'){
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.nav.sidebar-nav li a[href="/contactus"]').addClass('active');
        }
        if (window.location.pathname == '/sell'){
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.nav.sidebar-nav li a[href="/sell"]').addClass('active');
        }
        if (window.location.pathname == '/buy' || window.location.pathname == '/all_asset_sale' || window.location.pathname == '/all_past_sale' || window.location.pathname == '/saved_sell' || window.location.pathname == '/selected_property_page'){
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.nav.sidebar-nav li a[href="/buy"]').addClass('active');
        }
        if (window.location.pathname == '/rent' || window.location.pathname == '/all_asset_lease' || window.location.pathname == '/all_past_lease'){
            $('.nav.sidebar-nav li a').removeClass('active');
            $('.nav.sidebar-nav li a[href="/rent"]').addClass('active');
        }
    });

    function same_listing_delete_and_saved_data($this,from_call){
        var html_content = $('html')
        var website_user_id = html_content.data('website_user_id');
        var logged_user_id = html_content.data('user_id');
        if(website_user_id == logged_user_id){
            var list = []
            function getCookie(cname) {
                var name = cname + "=";
                var ca = document.cookie.split(';');
                for(var i=0; i<ca.length; i++) {
                    var c = ca[i];
                    while (c.charAt(0)==' ') c = c.substring(1);
                    if (c.indexOf(name) == 0)
                    {
                        list.push(c.substring(name.length, c.length));
                    }
                }
                return "";
            }
            var product_id = getCookie("property_id");
            var lease_id = $this.data('lease_id');
            var lease_id_str = lease_id.toString();
            var list_first_value = list[0]
            var list_update_new = list_first_value.split(',');
            list_update_new.splice( $.inArray(lease_id_str, list_update_new), 1 );
            function setCookie(cname, cvalue, exdays) {
                var name = cname + "=";
                var d = new Date();
                d.setTime(d.getTime() + (exdays*24*60*60*1000));
                var expires = "expires="+d.toUTCString();
                document.cookie = cname + "=" + cvalue + "; " + expires;
            }
            var create_cookie = setCookie("property_id", list_update_new, 365);
            displayTotalCookieProducts()

            if (from_call == 'listing-delete'){
                var parent_div =$this.parent().parent().parent().parent()
                $(parent_div).attr('style', 'display:none');
            }
            if (from_call == 'listing-saved-data'){
                var parent_div =$this.parent()
                var second_img = jQuery(parent_div).children(".listing-save");
                second_img.data('check_value', 'true');
                $this.attr('style', 'display: none');
                $(second_img).attr('style', 'display:block; cursor:pointer;');
            }
        }
        if(website_user_id != logged_user_id){
            var lease_id = $this.data('lease_id');
            odoo.jsonRpc("/change_fav_property", 'call', {
                'fav_property': lease_id
            }).then(function(data) {
                displayTotalCookieProducts()
                if (from_call == 'listing-delete'){
                    var parent_div = $this.parent().parent().parent().parent()
                    $(parent_div).attr('style', 'display:none');
                }
                if (from_call == 'listing-saved-data'){
                    var parent_div =$this.parent()
                    var second_img = jQuery(parent_div).children(".listing-save");
                    second_img.data('check_value', 'true');
                    $this.attr('style', 'display: none');
                    $(second_img).attr('style', 'display:block; cursor:pointer;');
                }
            });
        }
    }
    //code for remove property id when click on filled heart button form saved page
    $(document).on('click', '.listing-delete', function(e){
        same_listing_delete_and_saved_data($(this),'listing-delete')
    });

    //code for remove property id when click on filled heart button form all page
    $(document).on('click', '.listing-saved-data', function(e){
        same_listing_delete_and_saved_data($(this),'listing-saved-data')
    });

    //code for hover and click eveent in sales and rent page property type dropdown
    $(document).on('mouseover', '.dropdown-submenu', function(e){
        $(this).find(".dropdown-menu").attr('style', 'display: block;');

        $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
        $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
    });

    $(document).on('mouseleave', '.dropdown-submenu', function(e){
        if ($(this).find(".dropdown-menu").hasClass('active')){
            $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
            $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
        }
        else{
            $(this).find(".fa.fa-caret-left").attr('style', 'display: none');
            $(this).find(".fa.fa-caret-down").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
            $(this).find(".dropdown-menu").attr('style', 'display: none;');
        }
    });

//    $(document).on('mouseover', '.dropdown-submenu .dropdown-menu', function(e){
//        $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
//        $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
//    });
//
//    $(document).on('mouseleave', '.dropdown-submenu .dropdown-menu', function(e){
//        $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
//        $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
//    });

    $(document).on('click', '.dropdown-submenu', function(e){
        var dorpdown_menu = $(this).children(".dropdown-menu");
        if ($(this).children(".dropdown-menu").hasClass('active')){
            $(this).children(".dropdown-menu").attr('style', 'display: none');
            $(this).children(".dropdown-menu").removeClass('active');
            $(this).find(".fa.fa-caret-left").attr('style', 'display: none');
            $(this).find(".fa.fa-caret-down").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
        }
        else{
            $(this).children(".dropdown-menu").attr('style', 'display: block');
            $(this).children(".dropdown-menu").addClass('active');
            $(this).find(".fa.fa-caret-down").attr('style', 'display: none;');
            $(this).find(".fa.fa-caret-left").attr('style', 'display: block;width:14px;float:left;margin-top: 3px;');
        }
    });

//    $("#menu-toggle").click(function(e) {
    $(document).on('click', '#menu-toggle', function(e){
        e.preventDefault();
        $("#wrapper").toggleClass("active");
    });

    if ($(window).width() <= 992) {
        $('.arrow-slidebar').children().children("i").addClass('fa-chevron-right');
       }
       else{
       $('.arrow-slidebar').children().children("i").addClass('fa-chevron-left');
       }
        $(document).on('click', '.social_share_property', function(e){
    });

//    $('#datetimepicker8').datepicker();
    $(document).bind('click', '.date_maintenance', function(e){
        $('#datetimepicker8').datepicker();
    });

    $(document).on('click', '.maintenane_type_class', function(e){
        $(this).parent('#inputTelType').find('.maintenane_type_class').removeClass('active')
        $(this).addClass('active')
    });

    // create Maintanance from perticular property page
    $(document).on('click', '#submit_maintanance', function(e){
        $('#MaintanancepropertyForm').validator('validate');
        if ($('#MaintanancepropertyForm').find('.has-error:visible').size() > 0) return;
        odoo.jsonRpc("/create_maintanance", 'call', {
            /*'type_id': $('#MaintanancepropertyForm #inputTelType .maintenane_type_class.active').data('type_id'),*/
            'type_id': $('#MaintanancepropertyForm #inputTelType .maintenane_type_class:selected').data('type_id'),
            'date': $('.date_maintenance').val(),
            'description': $('#MaintanancepropertyForm #inputMsg').val(),
            'property_id': $('#MaintanancepropertyForm').data('property_id'),
            'renters_fault': $('#renters_fault').is( ':checked' ),
        }).then(function() {
            $('#MaintanancepropertyForm')[0].reset();
            $("#MaintanancepropertyForm #display_success_msg").css('display', 'block');
        });
    });


});
});

