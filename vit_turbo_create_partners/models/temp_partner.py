from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
import traceback
import json

class temp_partner(models.Model):
    _name = 'vit.temp_partner'
    _description = 'Temp Partner'


    name = fields.Char(string="Name")
    invoice_warn = fields.Char(string="Invoce Warn")
    sale_warn = fields.Char()
    active = fields.Boolean(string="Active", default=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    picking_warn = fields.Char(string="Picking Warn")
    purchase_warn = fields.Char(string="Purchase Warn")
    # email = fields.Char(string="Email")

    state = fields.Selection(string="State", selection=[('draft','Draft'),('imported','Imported')], default="draft")


    # @api.model_cr
    def init(self):
        _logger.info("creating functions...")
        self.env.cr.execute("""DROP FUNCTION IF EXISTS vit_create_partners(TEXT);
        CREATE OR REPLACE FUNCTION vit_create_partners(data TEXT)
        RETURNS VOID AS $BODY$
        DECLARE
            records TEXT[];
            rec TEXT;
            partner_rec TEXT[];
            v_name TEXT;
            v_invoice_warn TEXT;
            v_sale_warn TEXT;
            v_active BOOLEAN;
            v_street TEXT;
            v_street2 TEXT;
            v_phone TEXT;
            v_mobile TEXT;
            v_picking_warn TEXT;
            v_purchase_warn TEXT;
            --v_date TEXT;
            --v_title TEXT;
        -- 	v_parent_name TEXT;
        -- 	v_ref TEXT;
        -- 	v_user_id TEXT;
        -- 	v_vat TEXT;
        -- 	v_comment TEXT;
        -- 	v_barcode TEXT;
        -- 	v_customer TEXT;
        -- 	v_supplier TEXT;
        -- 	v_employee TEXT;
        -- 	v_function TEXT;
        -- 	v_type TEXT;
            v_partner_exist INTEGER;
            
        BEGIN
            SELECT string_to_array(data, '|') INTO records;
            FOREACH rec IN ARRAY records LOOP
                SELECT string_to_array(rec, '~~') INTO partner_rec;
                v_name = partner_rec[1];
                v_invoice_warn = partner_rec[2];
                v_sale_warn = partner_rec[3];
                v_active = partner_rec[4];
                v_street = partner_rec[5];
                v_street2 = partner_rec[6];
                v_phone = partner_rec[7];
                v_mobile = partner_rec[8];
                v_picking_warn = partner_rec[9];
                v_purchase_warn = partner_rec[10];
                --v_date = partner_rec[2];
                --v_title = partner_rec[3];
        -- 		v_parent_name = partner_rec[4];
        -- 		v_ref = partner_rec[5];
        -- 		v_user_id = partner_rec[6];
        -- 		v_vat = partner_rec[7];
        -- 		v_comment = partner_rec[8];
        -- 		v_barcode = partner_rec[9];
        -- 		v_customer= partner_rec[11];
        -- 		v_supplier= partner_rec[12];
        -- 		v_employee= partner_rec[13];
        -- 		v_function= partner_rec[14];
        -- 		v_type = partner_rec[15];

                SELECT id from res_partner where name = v_name INTO v_partner_exist;

                IF v_partner_exist IS NULL THEN

                    -- insert res_partner
                    insert into res_partner (
                        name,
                        display_name,
                        invoice_warn,
                        sale_warn,
                        active,
                        street,
                        street2,
                        phone,
                        mobile,
                        picking_warn,
                        purchase_warn
                        --date,
                        --title,
        -- 				parent_id,
        -- 				ref,
        -- 				user_id,
        -- 				vat,
        -- 				comment ,
        -- 				barcode ,			
        -- 				customer,
        -- 				supplier,
        -- 				employee,
        -- 				function,
        -- 				type
                    )
                    values (
                        v_name,
                        v_name,
                        v_invoice_warn,
                        v_sale_warn,
                        v_active,
                        v_street,
                        v_street2,
                        v_phone,
                        v_mobile,
                        v_picking_warn,
                        v_purchase_warn
                        --v_date,
                        --v_title,
        -- 				(select id from res_partner where name = v_parent_name),
        -- 				v_ref,
        -- 				(select id from res_users where login = v_user_id),
        -- 				v_vat,
        -- 				v_comment ,
        -- 				v_barcode ,
        -- 				v_customer,
        -- 				v_supplier,
        -- 				v_employee,
        -- 				v_function,
        -- 				v_type
                    );

                ELSE
                    UPDATE res_partner SET
                        name=v_name,
                        display_name=v_name,
                        invoice_warn=v_invoice_warn,
                        sale_warn=v_sale_warn,
                        active=v_active,
                        street=v_street,
                        street2=v_street2,
                        phone=v_phone,
                        mobile=v_mobile,
                        picking_warn=v_picking_warn,
                        purchase_warn=v_purchase_warn
                        --date=v_date,
                        --title=v_title,
        -- 				parent_name=v_parent_name,
        -- 				ref=v_ref,
        -- 				user_id=v_user_id,
        -- 				vat=v_vat,
        -- 				comment=v_comment,
        -- 				barcode=v_barcode,
        -- 				active=v_active,
        -- 				customer=v_customer,
        -- 				supplier=v_supplier,
        -- 				employee=v_employee,
        -- 				function=v_function,
        -- 				type=v_type
                    WHERE
                        id=v_partner_exist;

                END IF;

                --RAISE NOTICE 'create partner %', v_first_name;

            END LOOP;
        END;

        $BODY$
        LANGUAGE plpgsql;

        """)

    def cron_import(self):
        self.process()
        
    @api.multi
    def process(self):
        

        try:
            start = time.time()
            cr = self.env.cr
            data = []
            for rec in self.env['vit.temp_partner'].search([('state','=','draft')]):
                data.append([
                    rec.name,
                    rec.invoice_warn,
                    rec.sale_warn,
                    rec.active,
                    rec.street,
                    rec.street2,
                    rec.phone,
                    rec.mobile,
                    rec.picking_warn,
                    rec.purchase_warn
                    # rec.state,
                    # rec.date,
                    # rec.title,
                    # rec.parent_name,
                    # rec.ref, 
                    # rec.user_id,
                    # rec.vat,
                    # rec.comment ,
                    # rec.barcode ,
                    # rec.customer,   
                    # rec.supplier,   
                    # rec.employee,
                    # rec.function,
                    # rec.type
                ])
            data_final, i = self.format_data(data)
            _logger.info(data_final)

            self.env.cr.execute("select vit_create_partners('%s')" % (data_final))
            _logger.info('sukses----------->>>>>>>>>>>>>')
            
            end = time.time()
            duration = end - start
            
            sql = "update vit_temp_partner set state = 'imported' where state='draft'"
            cr.execute(sql)
            
            return json.dumps({'status': 'OK' , 'message' : 'Created %d Employees in %s seconds' % (i, duration)})

        except Exception as e :
            self.env.cr.rollback()
            trc = traceback.format_exc()
            _logger.error(trc)
            return json.dumps({'status': 'Failed' , 'message': str(trc)})        

    """
    API to create employees
    data is an array containing temp_partner records :
    [[emp_no,first_name,last_name,birth_date,gender,hire_date,department],
    [emp_no,first_name,last_name,birth_date,gender,hire_date,department],...]
    """
    @api.multi
    def batch_create_partners(self):
        try:
            start = time.time()
            cr = self.env.cr
            data=[]
            data_final, i = self.format_data(data)
            _logger.info(data_final)

            cr.execute("select vit_create_emp(%s)", (data_final,))

            end = time.time()
            duration = end - start
            return json.dumps({'status': 'OK' , 'message' : 'Created %d Employees in %s seconds' % (i, duration)})

        except Exception as e :
            self.env.cr.rollback()
            trc = traceback.format_exc()
            _logger.error(trc)
            return json.dumps({'status': 'Failed' , 'message': str(trc)})

    """
    convert array [ [], [], ... ] to string f1~~f2~~f3|f1~~f2~~f3|...
    """
    def format_data(self, data):
        i = 0
        data_final=[]
        for el in data:
            recs = [str(d) for d in el]
            recs = "~~".join(recs)
            data_final.append(recs)
            i = i + 1
        data_final = "|".join(data_final)
        return data_final, i