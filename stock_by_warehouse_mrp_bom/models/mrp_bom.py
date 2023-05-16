from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    warehouses_stock = fields.Text(store=False, readonly=True)
    warehouse_id = fields.Many2one(string="Warehouse", related="bom_id.picking_type_id.warehouse_id")
    warehouses_stock_recompute = fields.Boolean(store=False, readonly=False)
    detailed_type = fields.Selection(related="product_id.detailed_type")

    def _compute_get_warehouses_stock(self):
        for line in self:
            line.warehouses_stock = line.product_id.with_context(
                warehouse_id=line.warehouse_id
            )._compute_get_quantity_warehouses_json()

    @api.onchange("warehouses_stock_recompute", "product_id")
    def _warehouses_stock_recompute_onchange(self):
        if not self.warehouses_stock_recompute:
            self.warehouses_stock_recompute = True
            return
        self.warehouse_id = self.bom_id.picking_type_id.warehouse_id
        self._compute_get_warehouses_stock()
        self.warehouses_stock_recompute = True
