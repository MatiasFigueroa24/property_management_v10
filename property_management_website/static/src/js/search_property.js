$(document).ready(function(){
    view = {};
    $('.basic_search input').each(function(){
        view[this.name] = this.value
    }) 
    view['type_of_property'] = $('#type_of_property').val();
    view['min_range'] = $('#min_price_range_id').val();
    view['max_range'] = $('#max_price_range_id').val();
    openerp.jsonRpc("/search_property", 'call', view).then(function(property_view) {
        $('#propertys_view').html(property_view);
        $('.fav_img').bootstrapToggle({
            on: 'Remove from favourites',
            off: 'Add to favourites',
          });
    });
    function property_search_common(e){
        var viewArr = $(e).closest('form').serializeArray(); 
        for ( var i in viewArr) {
            view[viewArr[i].name] = viewArr[i].value;
        }
        var list = false;
        if($('.btn_list').hasClass('active')){
            var list = true;
        }
        openerp.jsonRpc("/search_property", 'call', view).then(function(property_view) {
            $('#propertys_view').html(property_view);
            $('.fav_img').bootstrapToggle({
                on: 'Remove from favourites',
                off: 'Add to favourites',
              });
            if(!list){
                $('#propertys_view').find('.btn_list').removeClass('active');
                $('#propertys_view').find('.btn_grid').addClass('active').click();
            }
        });
    }
    $('.btn_property_filter').click(function(){
        property_search_common(this)
    })
    $('.dropdown_filter_change').change(function() {
        property_search_common(this);
    });
    
    $(document).on('click', '.products_pager ul li a', function(e){
        e.preventDefault();
        var viewArr = $('.btn_property_filter').closest('form').serializeArray(); 
        for ( var i in viewArr) {
            view[viewArr[i].name] = viewArr[i].value;
        }
        var list = false;
        if($('.btn_list').hasClass('active')){
            var list = true;
        }
        if ($(this).text() == 'Next'){
            view['page'] = parseInt($('.products_pager ul li.active a')[0].text) + 1;
        }else if($(this).text() == 'Prev'){
            view['page'] = parseInt($('.products_pager ul li.active a')[0].text) - 1;
        }else{
            view['page'] = $(this).text();
        }
        openerp.jsonRpc("/search_property", 'call', view).then(function(property_view) {
            $('#propertys_view').html(property_view);
            $('.fav_img').bootstrapToggle({
                on: 'Remove from favourites',
                off: 'Add to favourites',
              });
            if(!list){
                $('#propertys_view').find('.btn_list').removeClass('active');
                $('#propertys_view').find('.btn_grid').addClass('active').click();
            }
        });
        
        
    })
    
});
