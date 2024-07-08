from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange, ServiceInfo
import socket
import netifaces
from core.utils.logger import HardwareMonitorLogger as Logger


logger = Logger(__name__).get_logger()


class ZeroConfService:
    def __init__(self, service_name, service_type, port):
        self.service_name = service_name
        self.service_type = service_type
        self.port = port
        self.zeroconf = Zeroconf()

        self.ip_address = self._get_ip_address()

        self.info = ServiceInfo(
            type_=self.service_type,
            name=f"{self.service_name}.{self.service_type}",
            addresses=[socket.inet_aton(self.ip_address)],
            port=self.port,
            properties={}
        )

    def _get_ip_address(self):
        try:
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    if ip != '127.0.0.1':
                        return ip
            raise Exception("Не удалось определить IP-адрес")
        except Exception as e:
            logger.error(f"Ошибка при получении IP-адреса: {e}")
            raise

    def start(self):
        self.zeroconf.register_service(self.info)
        logger.info(f"Сервис '{self.service_name}' зарегистрирован на порту {self.port}")

    def stop(self):
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
        logger.info(f"Сервис '{self.service_name}' остановлен")
