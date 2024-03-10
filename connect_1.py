from netmiko import ConnectHandler # CONNECTIONS
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException # CONNECTIONS
from paramiko import SSHException # CONNECTIONS
from getpass4 import getpass # MANAGE PASSWORD
from datetime import datetime # DATE AND TIME INFORMATION
from os.path import exists # TO CHECK FILES ON THE SYSTEM
import pyfiglet # FORMAT TEXT
from colorama import Fore, Style # TO SET COLOURS IN TERMINAL VIEW
import yaml #  TO WORK WITH YALM FILES

class ConnectAndPush:
   
   def __init__(self):

      self.ascii_banner = pyfiglet.figlet_format("SSH con Netmiko\n") # BANNER
      self.archivos_conf = True
      self.user=input('User Please: ')
      self.clave=getpass('Password Please: ')

      
      if (exists('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/DEVICE.yaml')): # CHECK IF THE FILE EXISTS
        self.ip_file='/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/DEVICE.yaml' # POPULEATE THE VARIALBLE ip_file
      else:
         print(Fore.RED + "La playlist de IP no esta disponible" + Style.RESET_ALL)
         self.archivos_conf = False
      
      try:
         with open(self.ip_file, 'r') as stream:
            self.dispositivos = yaml.safe_load(stream)
      except FileNotFoundError:
            print(Fore.RED + "The DEVICE.yaml file is not found." + Style.RESET_ALL)
            self.archivos_conf = False
     
      if (exists('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/COMMANDS.txt')): # CHECK IF THE FILE EXISTS
         self.command_file='/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/DATA/COMMANDS.txt' # POPULATE THE VARIALBLE command_file 
      else:
         print(Fore.RED + "El archivo de Comandos no esta disponible" + Style.RESET_ALL)
         self.archivos_conf = False

   def conectar(self):
      if (self.archivos_conf):
         print(Fore.MAGENTA + self.ascii_banner + "\n" + Style.RESET_ALL)
         equipos=open(self.ip_file)
         fecha = datetime.now().strftime("%Y%m%d")
         
         comandos=open(self.command_file)  # POPULATE THE VARIABLE comandos WITH THE EXECUTION COMMNADS
         
         for device_name, device_info in self.dispositivos.items():
            host = device_info.copy()
            host['username']=self.user
            host['password']=self.clave
            print(Fore.LIGHTGREEN_EX + '\nConectandose a:' + device_name + ': ' + host['ip'] + Style.RESET_ALL)
            print('- - - - - - - - - - - -\n')
            
            try:
               hora = datetime.now().strftime("%H:%M:%S")   # CURRENT TIME
               ssh = ConnectHandler(**host)
               resultado=open('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/RESULT/'+fecha+'-resultados.txt', 'a')
               # DEVICE TITLE - HEADER
               resultado.write('\n- - - - - - - - - - -\n')
               resultado.write('\n' + hora + ' --> ' + device_name + ': ' + host['ip'])
               # EXECUTION OF COMMANDS
               for coma in comandos:
                  salida = ssh.send_command(coma)
                  resultado.write('\n- - -' + coma + '- - -\n' + salida + '\n')
                  print(coma)
               # CONNECTION CLOSE
               ssh.disconnect()
               # CLOSE FILE
               resultado.close()

            except (NetmikoTimeoutException, NetmikoAuthenticationException, SSHException) as e:
               error=open('/mnt/g/Otros ordenadores/Mi portátil/DEVNET/AUTOMATION/CONEC_TEST/RESULT/'+fecha+'-errores.txt', 'a')
               error.write('\n- - - - - - - - - - -\n' + hora + ' --> ' + str(e)) # TELL US THE ERROR
               error.close()
               continue
            
      print('Verifique si los archivos de configuración esten en la carpeta de RESULTADOS.')

if __name__ == '__main__':
   ConnectAndPush().conectar()