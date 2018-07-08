# -*- coding: utf-8 -*-

import socket
import platform
import threading
import time
from PortScanner import constants
class PortScanner:
    # default ports to be scanned is top 1000
    __port_list_top_1000 = constants.port_list_top_1000
    __port_list_top_100 = constants.port_list_top_100
    __port_list_top_50 = constants.port_list_top_50

    # default thread number limit
    __thread_limit = 100

    # default connection timeout time in seconds
    __delay = 10


    @classmethod
    def __usage(cls):
        """
        Return the usage information for invalid input host name.
        """
        print('python Port Scanner v0.1')
        print('please make sure the input host name is in the form of "something.com" or "http://something.com!"\n')

    def __init__(self, target_ports=None):
        """
       PortScanner对象的构造函数。 如果target_ports是列表，则此端口列表将用作
         要扫描的端口列表。 如果target_ports是int，则应该是50,100或1000，表示
         将使用哪个默认列表。

         ：param target_ports：如果这个args是一个列表，那么这个要扫描的端口列表，
         默认为self .__ port_list_top_1000。 如果这个args是一个int，那么它应该是50,100或1000.并且
         将分别使用相应的默认列表。
         ：type target_ports：list或int
        """
        if target_ports is None:
            self.target_ports = self.__port_list_top_1000
        elif type(target_ports) == list:
            self.target_ports = target_ports
        elif type(target_ports) == int:
            self.target_ports = self.check_default_list(target_ports)

    def check_default_list(self, target_port_rank):
        """
     	 检查输入目标端口等级。 目标端口等级应为50,100或1000。
         对于有效输入，将返回相应的端口列表。

         ：param target_port_rank：top K要返回的常用端口列表。
         ：return：top K常用端口列表。
        """
        if (
            target_port_rank != 50 and
            target_port_rank != 100 and
            target_port_rank != 1000
        ):
            raise ValueError(
                'Invalid port rank {}. Should be 50, 100 or 1,000.'.format(target_port_rank)
            )

        if target_port_rank == 50:
            return self.__port_list_top_50
        elif target_port_rank == 100:
            return self.__port_list_top_100
        else:
            return self.__port_list_top_1000

    def scan(self, host_name, message=''):
        """
        这是需要调用以执行端口扫描的功能

         ：param host_name：要扫描的主机名
         ：param message：将包含在扫描数据包中的消息
         为了防止道德问题（默认：''）。
         ：return：一个dict对象，包含给定主机的扫描结果
         {port_number：status}
         ：rtype：dict
        """
        host_name = str(host_name)
        if 'http://' in host_name or 'https://' in host_name:
            host_name = host_name[host_name.find('://') + 3:]

        print('*' * 60 + '\n')
        print('start scanning website: {}'.format(host_name))

        try:
            server_ip = socket.gethostbyname(host_name)
            print('server ip is: {}'.format(str(server_ip)))

        except socket.error:
            # If the DNS resolution of a website cannot be finished, abort that website.
            print('hostname {} unknown!!!'.format(host_name))
            self.__usage()
            return {}
            # May need to return specific value to indicate the failure.

        start_time = time.time()
        output = self.__scan_ports(server_ip, self.__delay, message.encode('utf-8'))
        stop_time = time.time()

        print('host {} scanned in  {} seconds'.format(host_name, stop_time - start_time))
        print('finished scan!\n')

        return output

    def set_thread_limit(self, limit):
        """
        设置端口扫描的最大线程数
         ：param limit：并发运行的最大线程数，默认为1000。
        """
        limit = int(limit)

        if limit <= 0 or limit > 50000:
            print(
                'Warning: Invalid thread number limit {}!'
                'Please make sure the thread limit is within the range of (1, 50,000)!'.format(limit)
            )
            print('The scanning process will use default thread limit 1,000.')
            return

        self.__thread_limit = limit

    def set_delay(self, delay):
        """
        设置端口扫描的超时延迟（以秒为单位）
         ：param delay：TCP套接字等待超时的时间（以秒为单位），默认为10秒。
        """
        delay = int(delay)
        if delay <= 0 or delay > 100:
            print(
                'Warning: Invalid delay value {} seconds!'
                'Please make sure the input delay is within the range of (1, 100)'.format(delay)
            )
            print('The scanning process will use the default delay time 10 seconds.')
            return

        self.__delay = delay

    def show_target_ports(self):
        """
       打印并返回正在扫描的端口列表。
         ：return：当前Scanner对象扫描的端口列表。
         ：rtype：列表
        """
        print ('Current port list is:')
        print (self.target_ports)
        return self.target_ports

    def show_delay(self):
        """
        打印并返回TCP套接字等待超时的延迟（以秒为单位）。
         ：return：TCP连接的超时时间间隔，单位为秒。
         ：rtype：int
        """
        print ('Current timeout delay is {} seconds.'.format(self.__delay))
        return self.__delay

    def show_top_k_ports(self, k):
        """
        打印并返回顶部K常用端口。 K应为50,100或1000。
         ：param k：将返回前K列表。
         ：键入k：int
         ：return：top K常用端口。
         ：rtype：列表
        """
        port_list = self.check_default_list(k)
        print('Top {} commonly used ports:'.format(k))
        print(port_list)
        return port_list

    def __scan_ports_helper(self, ip, delay, output, message):
        """
         ：param ip：正在扫描的IP地址
         ：输入ip：str
         ：param delay：TCP套接字等待超时的时间（以秒为单位）
         ：type delay：int
         ：param output：一个dict，用于存储{port，status}样式对的结果。
         状态可以是“打开”或“关闭”。
         ：type输出：dict
         ：param message：将包含在扫描包中的消息，
         为了防止道德问题，默认为''。
         ：输入消息：str
        """
        port_index = 0

        while port_index < len(self.target_ports):
            # Ensure the number of concurrently running threads does not exceed the thread limit
            while threading.activeCount() < self.__thread_limit and port_index < len(self.target_ports):
                # Start threads
                thread = threading.Thread(target=self.__TCP_connect,
                                          args=(ip, self.target_ports[port_index], delay, output, message))
                thread.start()
                port_index = port_index + 1
            time.sleep(0.01)

    def __scan_ports(self, ip, delay, message):
        """
         ：param ip：正在扫描的IP地址
         ：输入ip：str
         ：param delay：TCP套接字等待超时的时间（以秒为单位）
         ：type delay：int
         ：param message：将包含在扫描包中的消息，
         为了防止道德问题，默认为''。
         ：输入消息：str
         ：return：存储结果{port，status}样式对的dict。
         状态可以是“打开”或“关闭”。
        """
        output = {}

        thread = threading.Thread(target=self.__scan_ports_helper, args=(ip, delay, output, message))
        thread.start()

        # Wait until all ports being scanned
        while len(output) < len(self.target_ports):
            time.sleep(0.01)
            continue

        # Print opening ports from small to large
        for port in self.target_ports:
            if output[port] == 'OPEN':
                print('{}: {}\n'.format(port, output[port]))

        return output

    def __TCP_connect(self, ip, port_number, delay, output, message):
        """
        使用TCP握手对给定IP地址上的给定端口执行状态检查
         ：param ip：正在扫描的IP地址
         ：输入ip：str
         ：param port_number：要检查的端口
         ：type port_number：int
         ：param delay：TCP套接字等待超时的时间（以秒为单位）
         ：type delay：int
         ：param output：一个dict，用于存储{port，status}样式对的结果。
         状态可以是“打开”或“关闭”。
         ：type输出：dict
         ：param message：将包含在扫描包中的消息，
         为了防止道德问题，默认为''。
         ：输入消息：str
        
         ＃根据不同的操作系统初始化TCP套接字对象。
         ＃除“Windows”以外的所有系统都一样。
        """
       
        curr_os = platform.system()
        if curr_os == 'Windows':
            TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCP_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            TCP_sock.settimeout(delay)
        else:
            TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCP_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            TCP_sock.settimeout(delay)

        # Initialize a UDP socket to send scanning alert message if there exists an non-empty message
        if message != '':
            UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP_sock.sendto(message, (ip, int(port_number)))

        try:
            result = TCP_sock.connect_ex((ip, int(port_number)))
            if message != '':
                TCP_sock.sendall(message)

            # If the TCP handshake is successful, the port is OPEN. Otherwise it is CLOSE
            if result == 0:
                output[port_number] = 'OPEN'
            else:
                output[port_number] = 'CLOSE'

            TCP_sock.close()

        except socket.error as e:
            # Failed to perform a TCP handshake means the port is probably close.
            output[port_number] = 'CLOSE'
            pass
