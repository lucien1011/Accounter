from collections import OrderedDict

class BaseClass(object):
    def __init__(self,name,**kwargs):
        self._name = name

        '''All keyword arguments are added as attributes.'''
        self.__dict__.update( kwargs )
        pass        
        
    def __str__(self):
        '''A useful printout'''
        header = '{type}: {name}'.format( type=self.__class__.__name__, name=self._name)
        varlines = ['\t{var:<15}:   {value}'.format(var=var, value=value) \
                    for var,value in sorted(vars(self).iteritems()) \
                    if var is not 'name']
        all = [ header ]
        all.extend(varlines)
        return '\n'.join( all )

class Payment(BaseClass):
    def __init__(self,name,**kwargs):
        super(Payment,self).__init__(name,**kwargs)

    def __str__(self):
        varlines =  ['{var:<15}:   {value}'.format(var=var, value=value) \
                    for var,value in sorted(vars(self).iteritems()) \
                    if var is not '_name']
        return '\n'.join(varlines)


class PaymentReader(BaseClass):
    def readTextFile(self,textFilePath):
        self.dict = OrderedDict()
        self.file = open(textFilePath,"r")
        lines = self.file.readlines()
        tempPaymentList = []
        for line in lines:
            if line.startswith("#"): continue
            if line == "\n": continue
            if line.startswith("Title: "):
                self.dict["Title"] = line.split(":")[1]
                continue
            tempPaymentList.append(self.readInfo(line))
        tempPaymentList.sort(key=lambda x: x.date)
        self.dict["payments"] = tempPaymentList

    def readInfo(self,line):
        infoList = line.split("|")
        tempDict = {
            "date"      : infoList[0],
            "place"     : infoList[1],
            "amount"    : float(infoList[2]),
            "currency"  : infoList[3],
            "who"  : infoList[4].replace("\n",""),
            }
        return Payment("payment",**tempDict)

    def finish(self):
        self.file.close()

class Calculator(BaseClass):
    @staticmethod
    def calculate(paymentList):
        results = {}
        total = {}
        dividents = []
        for payment in paymentList:
            if payment.who not in dividents:
                dividents.append(payment.who)
            if payment.currency not in total:
                total[payment.currency] = 0.
            if (payment.who,payment.currency) not in results:
                results[(payment.who,payment.currency)] = 0.
            total[payment.currency] += payment.amount
            results[(payment.who,payment.currency)] += payment.amount
        for currency,totalAmount in total.iteritems():
            for divident in dividents:
                results[(divident,currency)] -= totalAmount/len(dividents)
        # Invert the sign to reflect the actual payment
        for key in results:
            results[key] *= -1.
        return results



         
