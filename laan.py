
class Laan:
	"""	
		Laan
		Beregn hvordan hvordan et annuitetslaan (fx realkreditlaan) afhaenger af forskellige parametre. 				

	"""

	def __init__(self, H=1000000, b=0.0, r=0.0025, ts=30,a = 0, f = 0.255):
		"""
		Dan Laan objekt. 

		Parametre: 
		----------
		H : float, valgfri
			Hovedstol. Beloeb som laanes.  
		b : float, valgfri
			Bidragssats: Hvis den paalydende/nominel bidrags pr. aar er 0.85\% og der fire terminer pr. aar, saa er bidragssatsen 0.85/4/100.  
		r : float, valgfri
			Rentesats: Hvis den paalydende/nominel rente pr. aar er 0.15\% og der fire terminer pr. aar, saa er rentesatsen 0.15/4/100.
		ts: int, valgfri
			Antal terminer i laanets loebetid. Hvis loebetiden er 30 aar og der er fire terminer pr. aar, saa er ts 4*30. 
		a: 	int, valgfri
			Antal terminer afdragsfrihed. 
		f: float, valgfri
			Fradragsprocent. Fra 2019 er fradragsprocenten ca. 25.5\%.  

		Returnerer
		----------
		Laan objekt med foelgende attributes:  
		.Bs :numpy.ndarray
			Array med bidragssats for hver termin. Index 1 er foerste termin. Ligeledes med .Rs/Af/Hs/Ys/YsS. 
		.Rs :numpy.ndarray   
			Array med bidragssats for hver termin. 
		.Af :numpy.ndarray   
			Array med afdrag (hvor meget laanet nedbringes) for hver termin. 
		.Hs :numpy.ndarray   
			Array med restgaeld for hver termin. 
		.Ys :numpy.ndarray   
			Array med ydelse (rente+bidrag+afdrag) foer skat for hver termin.
		.YsS :numpy.ndarray   
			Array med ydelse (rente+bidrag+afdrag) efter skat for hver termin. Fra 2019 er rentesatsen ca. 25.5\%. 
		.ts : int
			Antal terminer i laanets loebetid.

		Eksempler:
		>>> Laan = Laan()
		>>> Laan.print_plan()
		>>>	ydelser_foer_skat = Laan.Ys
		>>>	ydelser_efter_skat = Laan.YsS

		>>> F5 = Laan(r=0.15/4/100, b=0.85/4/100)
		>>> F10 = Laan(r=1.0/4/100, b=0.85/4/100)
		>>> forskelle_i_ydelse_efter_skat= F10.YsS-F5.YsS 
		>>> forskel_i_samlede_ydelse_efter_skat= F10.YsS.sum()-F5.YsS.sum() 

		>>> F5 = RealKreditLaan(r=0.15/4/100, b=0.85/4/100)
		>>> F5.skift(n=5*4,r=2.0/4/100,b=0.85/4/100)		
		>>> print "Foerste ydelse efter refinansiering foer skat: ", F5.Ys[5*4]
				"""
		import numpy as np
		from matplotlib import pylab as plt

		self.ts = ts
		self.Bs = np.zeros(ts+1) #bidrag
		self.Rs = np.zeros(ts+1) #rente
		self.Af = np.zeros(ts+1) #afbetaling
		self.Hs = np.zeros(ts+1) #restgaeld
		self.Hs[0] = float(H)
		self.Ys = np.zeros(ts+1) # ydelse (inkl. bidrag)
		self.YsS = np.zeros(ts+1) # ydelse (inkl. bidrag) efter skat
#		self.Ps = np.zeros(ts+1)
		self.annuitet(float(H),float(b), float(r), f=float(f), n=1, a = int(a))

	def annuitet(self, H, b, r, n=1, f = 0.255, a=0): 
		# fremskriv med afdragsfrihed
		while n<=a:
			rs = H*r # rente
			bs = H*b # bidrag
			self.Bs[n] = bs # bidrag
			self.Rs[n] = rs # rente
			self.Af[n] = 0.0 # afdrag
			self.Hs[n] = H # restgaeld
			self.Ys[n] = rs+bs  # ydelse
			self.YsS[n] = (rs+bs)*(1-f) # ydelse efter skat
			n+= 1
		#beregn ydelse foer bidragsats med afdrag
		y = H*r/((1.0-((1.0+r)**(-(self.ts-n)))))
		#fremskriv med rente
		while n<=self.ts:
			rs = H*r # rente
			bs = H*b # bidrag
			af = y-rs #afdrag
			H-=af #restgaeld
			self.Bs[n] = bs
			self.Rs[n] = rs
			self.Af[n] = af
			self.Hs[n] = H
			self.Ys[n] = y+bs
			self.YsS[n] = (y-af+bs)*(1-f)+af
			n+= 1
	def skift(self, n=0, b=0.0, r=0.0025, f=0.255, a =0):
		"""
		Simuler aendring i rente og bidrag. 
		Argumenter:
		n: int 		
			Terminstal renten aendres ved. 
		r: float
			Ny rentesats. 
		b: float
			Ny bidragsats. 
		f:	float
			Nyt rentefradrag. 
		"""
		self.annuitet(self.Hs[n],b,r,n=n, f=f, a = a )

	def print_plan(self, startaar= 2019, termin = 0, terminer_pr_aar=4): 
		print "termin/aar\tydelse(foer skat)\tydelse(eft. skat)\tafdrag\trestgaeld"
		for n in range(self.ts):
			print "%d/%d:\t\t%.0f\t\t\t%.0f\t\t\t%.0f\t%.0f"%(n%terminer_pr_aar+termin, startaar+n/4, self.Ys[n],self.YsS[n],self.Af[n], self.Hs[n])




