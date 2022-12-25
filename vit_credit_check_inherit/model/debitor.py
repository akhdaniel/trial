#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import logging
_logger = logging.getLogger(__name__)
import traceback
import json
import time


class debitor(models.Model):
    _name = "vit.debitor"
    _inherit = "vit.debitor"

    def init(self):
        _logger.info("creating functions...")
        self.env.cr.execute("""DROP FUNCTION IF EXISTS vit_create_debitors(TEXT);
        CREATE OR REPLACE FUNCTION vit_create_debitors(data TEXT)
        RETURNS VOID AS $BODY$
        DECLARE
            records TEXT[];
            rec TEXT;
            debitor_rec TEXT[];

            v_name TEXT;
            v_address TEXT;
            v_city TEXT;
            v_country TEXT;
            v_phone TEXT;
            v_mobile TEXT;
            v_email TEXT;
            v_debitor_exist INTEGER;
            v_credit_score TEXT;
            
        BEGIN
            SELECT string_to_array(data, '|') INTO records;
            FOREACH rec IN ARRAY records LOOP
                SELECT string_to_array(rec, '~~') INTO debitor_rec;

                v_name = debitor_rec[1];
                v_address = debitor_rec[2];
                v_city = debitor_rec[3];
                v_country = debitor_rec[4];
                v_phone = debitor_rec[5];
                v_mobile = debitor_rec[6];
                v_email = debitor_rec[7];
                SELECT 'COL-'||floor(random() * 5 + 1)::int into v_credit_score;

                SELECT id from vit_debitor where name = v_name INTO v_debitor_exist;

                IF v_debitor_exist IS NULL THEN

                    -- insert vit_debitor
                    insert into vit_debitor (
                        name,
                        address,
                        city,
                        country,
                        phone,
                        mobile,
                        email,
                        credit_score  
                    )
                    values (
                        v_name,
                        v_address,
                        v_city,
                        v_country,
                        v_phone,
                        v_mobile,
                        v_email,
                        v_credit_score
                    );

                ELSE
                    UPDATE vit_debitor SET
                        name=v_name,
                        address=v_address,
                        city=v_city,
                        country=v_country,
                        phone=v_phone,
                        mobile=v_mobile,
                        email=v_email,
                        credit_score=v_credit_score
                    WHERE
                        id=v_debitor_exist;

                END IF;

            END LOOP;
        END;

        $BODY$
        LANGUAGE plpgsql;

        """)


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


    def dummy_create_debitors(self, starting_index=0, quantity=1000):
        try:
            _logger.info('starting_index=%s, quantity=%s', starting_index, quantity)
            start = time.time()
            cr = self.env.cr

            data=[[
                'Debitor {}'.format(x),
                'Street Partner {}'.format(x),
                'City {}'.format(x),
                'Indonesia',
                '8120000000{}'.format(x),
                '8120000000{}'.format(x),
                'debitor{}@email.com'.format(x)
            ] for x in range(starting_index, starting_index+quantity)]

            data_final, i = self.format_data(data)

            cr.execute("select vit_create_debitors(%s)", (data_final,))

            end = time.time()
            duration = end - start
            res = {'status': 'OK' , 'message' : 'Created %d Debitors in %s seconds' % (i, duration)}
            _logger.info(res)
            return json.dumps(res)

        except Exception as e :
            self.env.cr.rollback()
            trc = traceback.format_exc()
            _logger.error(trc)
            return json.dumps({'status': 'Failed' , 'message': str(trc)})
