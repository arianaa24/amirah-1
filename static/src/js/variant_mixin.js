odoo.define('amirah.VariantMixin', function (require) {
'use strict';
    
var VariantMixin = require('website_sale.VariantMixin');

const originalOnChangeCombination = VariantMixin._onChangeCombination;

VariantMixin._onChangeCombination = function (ev, $parent, combination) {
    var $message = $parent.find(".availability_messages");
    var ajax = require('web.ajax');
    var params = {'producto': combination.product_id,};
    var route = '/sale/get_combination_existencias';

    ajax.jsonRpc(route, 'call', params).then(function (result) {
        $( ".amirah-mensaje" ).remove();
        $message.after( "<strong class='amirah-mensaje'>" + result + "</strong>" );
    });

    originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};

return VariantMixin;
});