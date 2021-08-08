import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app
from database.models import setup_db, Procedure, Worker, Inputs,Fields# Tokens are formatted as such to limit lenght on a line
FARM_MANAGER =('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjloTUNJTXphdFVnaWxld2F0b0o1cyJ9.eyJpc3MiOiJodHRwczovL21hdXJlZW4tZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBiN2QzOGYwNWU1NzQwMDcwZjljYjYyIiwiYXVkIjoiZmFybSIsImlhdCI6MTYyODQ1MTM0NywiZXhwIjoxNjI4NTM3NzQ3LCJhenAiOiJhaVV2OHJQQ0RiSTR1NTlhd0MwUXk3VHY4d3hWSmp1TiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmZpZWxkcyIsImdldDppbnB1dHMiLCJnZXQ6cHJvY2VkdXJlcyIsImdldDp3b3JrZXJzIiwicGF0Y2g6ZmllbGRzICIsInBhdGNoOmlucHV0cyIsInBhdGNoOndvcmtlcnMiLCJwb3N0OmZpZWxkcyIsInBvc3Q6aW5wdXRzIiwicG9zdDpwcm9jZWR1cmVzIiwicG9zdDp3b3JrZXJzIl19.Ocy2dM2ywf_8rZ0H_0ZyMu8CWpJXtnFOPXeR1sV4v4W0T7Wh0tqhDvwOTLQxsSZkdYbV6CiaHKSoVZOGGRrvh1YOd6LMAaVZI9ZGkawn_Os287q5Vsf_tSsHtwqGb1K7Nd1aPNu3ILNTLmDs0KZh2qv3_j2fuwry5s2aVACdQoKgJTiQNUZFyf2crWwaeW12Y3sTaAy490vhijionXSOB577f1L215DIy_ssMtgH9lFcv-EWfGYD_6bMYNnLu0lGqpQgipkaeREfbWEofGpMLMGAnAX1Q8qQ87a-z2xizVUNsGr00FAoVtCckCBNimYekdPYlupSh81b7bxxsnv4ew')
MANAGER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjloTUNJTXphdFVnaWxld2F0b0o1cyJ9.eyJpc3MiOiJodHRwczovL21hdXJlZW4tZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBmOTdhZTgzNTgyYmMwMDY5NDU3OTA4IiwiYXVkIjoiZmFybSIsImlhdCI6MTYyODQ1MTQwMiwiZXhwIjoxNjI4NTM3ODAyLCJhenAiOiJhaVV2OHJQQ0RiSTR1NTlhd0MwUXk3VHY4d3hWSmp1TiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmZpZWxkcyIsImRlbGV0ZTppbnB1dHMiLCJkZWxldGU6cHJvY2VkdXJlcyIsImRlbGV0ZTp3b3JrZXJzIiwiZ2V0OmZpZWxkcyIsImdldDppbnB1dHMiLCJnZXQ6cHJvY2VkdXJlcyIsImdldDp3b3JrZXJzIiwicGF0Y2g6ZmllbGRzICIsInBhdGNoOmlucHV0cyIsInBhdGNoOnByb2NlZHVyZXMiLCJwYXRjaDp3b3JrZXJzIiwicG9zdDpmaWVsZHMiLCJwb3N0OmlucHV0cyIsInBvc3Q6cHJvY2VkdXJlcyIsInBvc3Q6d29ya2VycyJdfQ.j4QisLE5rUEyL1L0Qo_FXqGkfoHnaDZhNDnsijatJaW1xB6fdrRwOdeRoPEwJ2e6kBJIRAjquXYSctRJWFqOkeXFtGqlt-K774vFseBGpL1pQBPFwCo1u6E0kePHv_ku72QflUTZU6ZaqGfz0vE1bgvK4f_gkNdFoojpGJ-3reRiWaMfgGAc_2yheU-ieHwBNbxvprWWElAKxej0wY5xrEopl1KKzDmx2-N-xmRZwBkdYq1qJYDLzX-KLFK9ioTr3_kBtSOJEijjTvApWPtcVY8cjAo8psgtBdVNHNSNTcb1iIXneIDh85KKkE5Jd5wG_tAwPFm7iVo7g_vlm65JMQ')

class ShambaTestCase(unittest.TestCase):
    """This class represents the shamba test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "shamba_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        # new procedure data 
        self.new_procedure = {
            "activity": "Fertilizer application",
            "date": "Wed, 10 Feb 2021 00:00:00 GMT",
            "field_id": 2,
            "image_link": "https://imagelink.com",
            "input_id": 1,
            "inputs_qty": 10,
            "name": "Testing Procedure",
            "worker_id": 1
        }
        self.patch_procedure= {
            'name': 'Farm Preparation', 
            'activity': "Weeding"
            }

         # new wrong procedure data 
        self.new_wrong_procedure = {
            "dates": "Wed, 10 Feb 2021 00:00:00 GMT",
            "field": 1,
        }

        # new input data 
        self.new_input = {
            "metrics": "Kg",
            "name": "CBDE Fertilizer",
            "quantity": 30
           }
        
        self.patch_inputs = {
            "metrics": "Tonnes",
            }

         # new wrong question data 
        self.new_wrong_input = {
            'question': 'Mathematics',
          
        }

         # new worker data 
        self.new_worker = {
            "name": "Bill Nyamu",
            "national_id":785784754,
            "phone_number":"+254637658475",
            "type": "Casual"
           }
        self.patch_workers = {
            "type": "Permanent"
           }

         # new wrong worker data 
        self.new_wrong_worker = {
            'question': 'Mathematics',
          
        }

          # new field data 
        self.new_field = {
            "name": "Field 1",
            "size": 1.4
           }

        self.patch_fields = {
            "name": "Field A",
     
           }

         # new wrong field data 
        self.new_wrong_field = {
            'question': 'Mathematics',
          
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

# # worker Test
    def test_create_new_worker(self):
        '''Test for successfull creation of a new worker'''
        res = self.client().post('/workers',
        json = self.new_worker,
        headers={'Authorization': f'Bearer {MANAGER}'})
       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['worker']))
        self.assertEqual(data['worker']['name'], 'Bill Nyamu')

    def test_retrieve_workers(self):
        '''Test retrieve workers, check the status code, success, and if there is data available '''
        res = self.client().get('/workers',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['workers']))

    def test_patch_workers(self):
        '''Test patch workers, check the status code, success, and if there is data available '''
        res = self.client().patch('/workers/1',
        json= self.patch_workers,
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['worker']))
        self.assertEqual(data['worker'][0]['type'], 'Permanent')
 

    def test_delete_worker(self):
                '''Test for successful deletion of a worker '''
                res = self.client().delete('/workers/5',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)

                worker = Worker.query.filter(Worker.id == 5).one_or_none()

                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertEqual(worker, None)

    def test_delete_worker_fail(self):
                    '''Test for failed deletion of a worker '''
                    res = self.client().delete('/workers/',
                    headers={'Authorization': f'Bearer {MANAGER}'})
                    data = json.loads(res.data)
                
                    self.assertEqual(res.status_code, 404)
                    self.assertEqual(data['success'], False)
                    self.assertEqual(data['message'], 'resource not found')

    def test_post_worker_with_no_params(self):
        '''Test for post for workers with no params passed to the api'''
        res= self.client().post('/workers',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')



# input tests 

    def test_create_new_input(self):
        '''Test for successfull creation of a new input'''
        res = self.client().post('/inputs',
        json = self.new_input,
        headers={'Authorization': f'Bearer {MANAGER}'})
       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['inputs']))
        self.assertEqual(data['inputs']['metrics'], 'Kg')




    def test_retrieve_inputs(self):
        '''Test retrieve input, check the status code, success, and if there is data available '''
        res = self.client().get('/inputs',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['inputs']))


    def test_patch_inputs(self):
        '''Test patch input, check the status code, success, and if there is data available '''
        res = self.client().patch('/inputs/1',
        json= self.patch_inputs,
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['input']))
        self.assertEqual(data['input'][0]['metrics'], 'Tonnes')
  
    def test_delete_input(self):
                '''Test for successful deletion of a input '''
                res = self.client().delete('/inputs/3',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)

                input = Inputs.query.filter(Inputs.id == 3).one_or_none()

                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertEqual(input, None)
  
    def test_delete_input_fail(self):
                '''Test for failed deletion of a input '''
                res = self.client().delete('/inputs/1000',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)
            
                self.assertEqual(res.status_code, 404)
                self.assertEqual(data['success'], False)
                self.assertEqual(data['message'], 'resource not found')

    def test_post_input_with_no_params(self):
        '''Test for post for inputs with no params passed to the api'''
        res= self.client().post('/inputs',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')




# fields tests

    def test_create_new_field(self):
        '''Test for successfull creation of a new field'''
        res = self.client().post('/fields',
        json = self.new_field,
        headers={'Authorization': f'Bearer {MANAGER}'})
       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['fields']))
        self.assertEqual(data['fields']['size'], 1.4)


    def test_retrieve_fields(self):
            '''Test retrieve fields, check the status code, success, and if there is data available '''
            res = self.client().get('/fields',
            headers={'Authorization': f'Bearer {MANAGER}'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['fields']))


    def test_patch_fields(self):
            '''Test patch fields, check the status code, success, and if there is data available '''
            res = self.client().patch('/fields/2',
             json= self.patch_fields,
            headers={'Authorization': f'Bearer {MANAGER}'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['field']))
            self.assertEqual(data['field'][0]['name'], 'Field A')


    def test_delete_field(self):
                '''Test for successful deletion of a field '''
                res = self.client().delete('/fields/7',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)

                field = Fields.query.filter(Fields.id == 7).one_or_none()

                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertEqual(field, None)

    
    def test_delete_field_fail(self):
                '''Test for failed deletion of a field '''
                res = self.client().delete('/fields/1000',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)
            
                self.assertEqual(res.status_code, 404)
                self.assertEqual(data['success'], False)
                self.assertEqual(data['message'], 'resource not found')

    def test_post_field_with_no_params(self):
        '''Test for post for procedures with no params passed to the api'''
        res= self.client().post('/fields',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
   

    





# Procedures

    def test_create_new_procedure(self):
        '''Test for successfull creation of a new procedure'''
        res = self.client().post('/procedures',
        json = self.new_procedure,
        headers={'Authorization': f'Bearer {MANAGER}'})
       
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['procedure']))
        self.assertTrue(data['created'])
        self.assertEqual(data['procedure']['name'], 'Testing Procedure')



    def test_retrieve_procedures(self):
        '''Test retrieve procedure, check the status code, success, and if there is data available '''
        res = self.client().get('/procedures',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_procedures'])
        self.assertTrue(len(data['procedures']))

    def test_patch_procedures(self):
            '''Test patch procedure, check the status code, success, and if there is data available '''
        
            res = self.client().patch(
                '/procedures/3',
                json= self.patch_procedure,
                headers={'Authorization': f'Bearer {MANAGER}'}
        )
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['procedure']))
            self.assertEqual(data['procedure'][0]['activity'], 'Weeding')


    def test_delete_procedures(self):
                '''Test for successful deletion of a procedures '''
                res = self.client().delete('/procedures/5',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)

                procedure = Procedure.query.filter(Procedure.id == 5).one_or_none()

                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertEqual(procedure, None)


# RBAC Farm Manager cannot delete a procedure
    def test_delete_procedures(self): 
                '''Test for successful deletion of a procedures '''
                res = self.client().delete('/procedures/5',
                headers={'Authorization': f'Bearer {FARM_MANAGER}'})
                data = json.loads(res.data)

                procedure = Procedure.query.filter(Procedure.id == 5).one_or_none()

                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertEqual(procedure, None)


   
    def test_delete_procedure_fail(self):
                '''Test for failed deletion of a procedure '''
                res = self.client().delete('/procedures/',
                headers={'Authorization': f'Bearer {MANAGER}'})
                data = json.loads(res.data)
            
                self.assertEqual(res.status_code, 404)
                self.assertEqual(data['success'], False)
                self.assertEqual(data['message'], 'resource not found')

    def test_post_procedures_with_no_params(self):
        '''Test for post for procedures with no params passed to the api'''
        res= self.client().post('/procedures',
        headers={'Authorization': f'Bearer {MANAGER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')

    
    def test_post_procedures_without_tokenheader(self):
        '''Test for post for procedures without token header passed to the api'''
        res= self.client().post('/procedures')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Authorization header is expected')

   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()