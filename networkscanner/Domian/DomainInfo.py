import dns.resolver

class domain_info:
    def __init__(self,url):
        self.domain = url
    def work(self):
    #domain = input("请输入域名地址:")       # 输入域名地址
    print('A记录：将主机名转换成IP地址')
    A = dns.resolver.query(self.domain, 'A')     # 指定查询记录为A型
    for i in A.response.answer:             # 通过response.answer方法获取查询回应信息
        # print(i)
        for j in i.items:
            print(i)    # 输出变量i中的内容
    print('MX记录：邮件交换记录，定义邮件服务器域名')
    MX = dns.resolver.query(self.domain, 'MX')   # 指定解析类型为MX记录
    for i in MX:                            # 遍历回应结果
        print('MX preference =', i.preference, 'mail exchanger =', i.exchange)
    #
    print('NS记录：标记区域的域名服务器及授权子域' )
    NS = dns.resolver.query(self.domain, 'NS')
    for i in NS.response.answer:
        for j in i.items:
            print(j.to_text())
