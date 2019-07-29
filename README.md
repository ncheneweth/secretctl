# secretctl
Command-line tool and module for working with aws secrets manager

<app>/<env>/<key> value, values

$ secretctl list di





 # s3 = session.client('s3')
 # for key in paginate(s3.list_objects_v2, Bucket='schlarpc-paginate-example'):
 #     print(key)


    #     try:
    #         resp = _session.describe_secret(SecretId=self.path)
    #         # if this does create except then secret already exists and this is an update
    #     except ClientError as e:
    #         # exception means secret does not already exist and we can create
    #
    #
    #
    #         try:
    #             response = secrets.describe_secret(SecretId=keyval)
    #             if binary == True:
    #                 response = client.update_secret(SecretId=keyval, SecretString=value)
    #             else:
    #                 response = client.update_secret(SecretId=keyval, SecretBinary=value)
    #         except ClientError as e:
    #             # this is a new secrets
    #             if binary == True:
    #                 response = secrets.create_secret(Name=keyval, SecretString=value)
    #             else:
    #                 response = secrets.create_secret(Name=keyval, SecretBinary=value)
    #
    # def get_secret(self, path):
    #     return str(path)
        # try:
        #     resp = self._session.get_secret_value(SecretId=path)
        #     if 'SecretString' in resp:
        #         return resp['SecretString']
        #     else:
        #         return base64.b64decode(resp['SecretBinary'])
        # except ClientError as e:
        #     raise e


     def paginate(method, **kwargs):
          client = method.__self__
          paginator = client.get_paginator(method.__name__)
          for page in paginator.paginate(**kwargs).result_key_iters():
              for result in page:
                  yield result

    # def resolve(self):
    #     if not self.path:
    #         print('no path')

    # def __setitem__(self):
    #     print('here')
    #     if not self.path:
    #         print('no path')
    #     if not self.key:
    #         print('no key')

    # def __getitem__(self, item):
    #     self.resolve()
    #     return self.value[item]

    # def __str__(self):
    #     self.resolve()
    #     if not self.value:
    #         raise RuntimeError('The secret could not be resolved')
    #     return str(self.value)
    #
    # @property
    # def is_binary(self):
    #     self.resolve()
    #     return 'binary' in self.value
