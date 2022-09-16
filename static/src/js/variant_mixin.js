odoo.define('amirah.VariantMixin', function (require) {
'use strict';
    
var VariantMixin = require('website_sale.VariantMixin');

const originalOnChangeCombination = VariantMixin._onChangeCombination;
VariantMixin._onChangeCombination = function (ev, $parent, combination) {
    console.log('Entra')
    console.log($parent)
    var rpc = require('web.rpc');
    var $message = $parent.find(".availability_messages");
    rpc.query({
        model: 'website',
        method: 'existencias',
        args: [[], combination.product_id]
    }).then(function (result) {
        $message.text(result);
    });

    originalOnChangeCombination.apply(this, [ev, $parent, combination]);
};


return VariantMixin;
});