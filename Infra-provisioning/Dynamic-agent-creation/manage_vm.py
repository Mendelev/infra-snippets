import sys
import os
import boto3

# Setup Credentials for AWS

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_REGION', 'us-east-1')  # Uses us-east-1 as default region if it is not specified

def criar_instancia(ami_id):
    try:  
      # Creating a session for boto3
      session = boto3.Session(
          aws_access_key_id=aws_access_key_id,
          aws_secret_access_key=aws_secret_access_key,
          region_name=aws_region
      )
  
      # Criar o cliente EC2
      ec2 = session.resource('ec2')
  
      # Criar a instância
      instancia = ec2.create_instances(
          ImageId=ami_id,
          InstanceType='t2.micro',
          MinCount=1,
          MaxCount=1,
          TagSpecifications=[
              {
                  'ResourceType': 'instance',
                  'Tags': [
                      {
                          'Key': 'Monitor',
                          'Value': 'True'
                      },
                  ]
              },
          ],
      )[0]
  
      #print("Instância criada com sucesso com o ID:", instancia.id)
      print(f'##vso[task.setvariable variable=INSTANCE_ID;isOutput=true]{instancia.id}')
      return instancia.id
    
    except Exception as e:
        print("Erro ao criar a instância:", e)
        sys.exit(1)

def excluir_instancia(instancia_id):
    try:
      # Criar uma sessão do boto3
      session = boto3.Session(
          aws_access_key_id=aws_access_key_id,
          aws_secret_access_key=aws_secret_access_key,
          region_name=aws_region
      )
  
      # Criar o cliente EC2
      ec2 = session.resource('ec2')
  
      # Obter a instância
      instancia = ec2.Instance(instancia_id)
  
      # Parar a instância antes de excluir
      instancia.stop()
  
      # Excluir a instância
      instancia.terminate()
  
      print("Instância", instancia_id, "excluída com sucesso.")
    except Exception as e:
        print("Erro ao criar a instância:", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python manager.py <opção>")
        print("Opções:")
        print("  criar <AMI_ID>: Cria uma instância EC2 a partir de uma AMI")
        print("  excluir <INSTANCE_ID>: Exclui a instância EC2 com o ID especificado")
        sys.exit(1)

    opcao = sys.argv[1]

    if opcao == "criar":
        if len(sys.argv) != 3:
            print("Uso: python manager.py criar <AMI_ID>")
            sys.exit(1)
        ami_id = sys.argv[2]
        instancia_id = criar_instancia(ami_id)
        with open("instance_id.txt", "w") as file:
            file.write(instancia_id)
    elif opcao == "excluir":
        if len(sys.argv) != 3:
            print("Uso: python manager.py excluir <INSTANCE_ID>")
            sys.exit(1)
        instancia_id = sys.argv[2]
        excluir_instancia(instancia_id)
    else:
        print("Opção inválida.")
        sys.exit(1)
