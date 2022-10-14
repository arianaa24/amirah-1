odoo.define('amirah.VariantMixin', function (require) {
'use strict';
    
var VariantMixin = require('website_sale.VariantMixin');

const originalOnChangeCombination = VariantMixin._onChangeCombination;
VariantMixin._onChangeCombination = function (ev, $parent, combination) {
    var rpc = require('web.rpc');
    var $message = $parent.find(".availability_messages");
    rpc.query({
        model: 'website',
        method: 'existencias',
        args: [[], combination.product_id]
    }).then(function (result) {
        $( ".amirah-mensaje" ).remove();
        $message.after( "<strong class='amirah-mensaje'>" + result + "</strong>" );
    });

    originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};

return VariantMixin;
});