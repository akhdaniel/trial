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
    active = fields.Boolean(string="Active", default=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
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
            v_active BOOLEAN;
            v_street TEXT;
            v_street2 TEXT;
            v_phone TEXT;
            v_mobile TEXT;
            v_partner_exist INTEGER;
            
        BEGIN
            SELECT string_to_array(data, '|') INTO records;
            FOREACH rec IN ARRAY records LOOP
                SELECT string_to_array(rec, '~~') INTO partner_rec;

                v_name = partner_rec[1];
                v_active = partner_rec[2];
                v_street = partner_rec[3];
                v_street2 = partner_rec[4];
                v_phone = partner_rec[5];
                v_mobile = partner_rec[6];

                SELECT id from res_partner where name = v_name INTO v_partner_exist;

                IF v_partner_exist IS NULL THEN

                    -- insert res_partner
                    insert into res_partner (
                        name,
                        display_name,
                        active,
                        street,
                        street2,
                        phone,
                        mobile                        
                    )
                    values (
                        v_name,
                        v_name,
                        v_active,
                        v_street,
                        v_street2,
                        v_phone,
                        v_mobile
                    );

                ELSE
                    UPDATE res_partner SET
                        name=v_name,
                        display_name=v_name,
                        active=v_active,
                        street=v_street,
                        street2=v_street2,
                        phone=v_phone,
                        mobile=v_mobile
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
        
    # @api.multi
    # process dari temp_partner 
    def process(self):

        try:
            start = time.time()
            cr = self.env.cr
            data = []
            for rec in self.env['vit.temp_partner'].search([('state','=','draft')]):
                data.append([
                    rec.name,
                    rec.active,
                    rec.street,
                    rec.street2,
                    rec.phone,
                    rec.mobile
                ])
            data_final, i = self.format_data(data)
            _logger.info(data_final)

            self.env.cr.execute("select vit_create_partners('%s')" % (data_final,))
            _logger.info('exectued----------->>>>>>>>>>>>>')
            
            end = time.time()
            duration = end - start
            
            sql = "update vit_temp_partner set state = 'imported' where state='draft'"
            cr.execute(sql)
            
            return json.dumps({'status': 'OK' , 'message' : 'Created %d Partners in %s seconds' % (i, duration)})

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
    # @api.multi
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
    
    
    def dummy_create_partners(self, quantity=1000):
        try:
            start = time.time()
            cr = self.env.cr
            data=[[
                'Partner {}'.format(x),
                True,
                'Street Partner {}'.format(x),
                'Street2 Partner {}'.format(x),
                '8120000000{}'.format(x),
                '8120000000{}'.format(x),
                'draft'
            ] for x in range(1,quantity)]
            data_final, i = self.format_data(data)
            _logger.info(data_final)

            cr.execute("select vit_create_partners(%s)", (data_final,))

            end = time.time()
            duration = end - start
            return json.dumps({'status': 'OK' , 'message' : 'Created %d Partners in %s seconds' % (i, duration)})

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