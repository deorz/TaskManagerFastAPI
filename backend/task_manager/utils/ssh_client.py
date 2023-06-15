from os import system

from paramiko import AutoAddPolicy, SSHClient, AuthenticationException, SSHException
from scp import SCPClient


class RemoteClient:

    def __init__(
        self,
        host: str,
        user: str,
        passphrase: str,
    ):
        self.host = host
        self.user = user
        self.passphrase = passphrase

    @property
    def connection(self):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                self.host,
                username=self.user,
                passphrase=self.passphrase,
                timeout=5000,
            )
            return client
        except AuthenticationException as e:
            print(e)
        except Exception as e:
            print(e)

    @property
    def scp(self) -> SCPClient:
        connection = self.connection
        return SCPClient(connection.get_transport())

    def disconnect(self):
        if self.connection:
            self.connection.close()
        if self.scp:
            self.scp.close()

    def download_file(self, filepath: str):
        self.scp.get(filepath)

    def upload_file(self, filepath: str, remote_path: str = '.'):
        self.scp.put(files=filepath, remote_path=remote_path)

    def execute_commands(self, command: str):
        return self.connection.exec_command(command=command)
