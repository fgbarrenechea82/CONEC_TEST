from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko import SSHException
from getpass4 import getpass
from datetime import datetime
from os.path import exists
import pyfiglet
from colorama import Fore, Style

class ConnectAndPush:
   
   def __init__(self):

      self.ascii_banner = pyfiglet.figlet_format("SSH con Netmiko\n") # BANNER
      self.archivos_conf = True
      self.user=getpass('User Please: ')
      self.clave=getpass('Password Please: ')

      if (exists('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/DEVICE.yaml')): # SI EXISTE UN ARCHIVO CON ESE NOMBRE EN LA RUTA DONDE ESTA EL PLAYLIST DE HOST
         self.ip_file='/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/DEVICE.yaml' # METELO EN LA VARIALBLE ip_file
      else:
         print(Fore.RED + "La playlist de IP no esta disponible" + Style.RESET_ALL)
         self.archivos_conf = False
      if (exists('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/COMMANDS.txt')): #  # SI EXISTE UN ARCHIVO CON ESE NOMBRE EN LA RUTA DONDE ESTA EL PLAYLIST CON LOS COMANDOS
         self.command_file='/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/COMMANDS.txt' # METELO EN LA VARIALBLE command_file 
      else:
         print(Fore.RED + "El archivo de Comandos no esta disponible" + Style.RESET_ALL)
         self.archivos_conf = False

   def conectar(self):
      if (self.archivos_conf):
         print(Fore.MAGENTA + self.ascii_banner + "\n" + Style.RESET_ALL)
         equipos=open(self.ip_file)
         fecha = datetime.now().strftime("%Y%m%d")

         for IP in equipos:
            comandos=open(self.command_file)  # VARIABLE QUE CARGA LOS COMANDOS A EJECUTAR
            host = {
               'device_type': 'cisco_ios', 
               'ip': '10.110.255.25',
               'port': '22',
               'username': self.user,
               'password': self.clave
            }
            print(Fore.LIGHTGREEN_EX + '\nConectandose a:' + host['ip'] + Style.RESET_ALL, end="")
            print('- - - - - - - - - - - -\n')
            
            try:
               hora = datetime.now().strftime("%H:%M:%S")   # ACTUALIZACION DE HORA
               ssh = ConnectHandler(**host)
               resultado=open('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/RESULT/'+fecha+'-resultados.txt', 'a')
               resultado.write('\n- - - - - - - - - - -\n\n' + hora + ' --> ' + host['ip'])
               for coma in comandos:
                  salida = ssh.send_command(coma)
                  resultado.write('- - -\n' + coma + '\n' + salida + '\n')
                  print('Ejecutando:', coma)
                  print(salida)
                  print("\n- - - - - - - - - -\n")
               ssh.disconnect()
               resultado.close()

            except (NetMikoTimeoutException, NetMikoAuthenticationException, SSHException) as e:
               print(e)
               error=open('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/RESULT/'+fecha+'-errores.txt', 'a')
               error.write('\n- - - - - - - - - - -\n' + hora + ' --> ' + str(e))   #INFORMA TIPO DE ERROR
               error.close()
               continue
      else:
         print('Verifique si los archivos de configuración esten en la carpeta de RESULTADOS.')


if __name__ == '__main__':
   ConnectAndPush().conectar()