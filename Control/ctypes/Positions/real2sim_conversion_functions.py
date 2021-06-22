
# REAL 2 SIM
def servo12_real2sim(pos12):
	if pos12>=583.3:
		targ12 = (140 - (6/25)*pos12)*(1.2/65)
	else:
		targ12 = -((6/25)*pos12 - 140)*(1/25)
	return targ12
def servo11_real2sim(pos11):
	if pos11>=750:
		targ11 = ((6/25)*pos11 - 180)*(1.5/60)
	else:
		targ11 = -(180 - (6/25)*pos11)*(0.6/40)
	return targ11

def servo32_real2sim(pos32):
	if pos32>=583.3:
		targ32 = (140 - (6/25)*pos32)*(1.2/65)
	else:
		targ32 = -((6/25)*pos32 - 140)*(1/25)
	return targ32
def servo31_real2sim(pos31):
	if pos31>=750:
		targ31 = ((6/25)*pos31 - 180)*(1.5/60)
	else:
		targ31 = -(180 - (6/25)*pos31)*(0.6/40)
	return targ31

def servo22_real2sim(pos22):
	if pos22>=416.6:
		targ22 = ((6/25)*pos22 - 100)*(1.2/65)
	else:
		targ22 = -(100 - (6/25)*pos22)*(1/25)
	return targ22
def servo21_real2sim(pos21):
	if pos21>=250:
		targ21 = (60 - (6/25)*pos21)*(1.5/60)
	else:
		targ21 = -((6/25)*pos21 - 60)*(0.6/60)
	return targ21

def servo42_real2sim(pos42):
	if pos42>=416.6:
		targ42 = ((6/25)*pos42 - 100)*(1.2/65)
	else:
		targ42 = -(100 - (6/25)*pos42)*(1/25)
	return targ42
def servo41_real2sim(pos41):
	if pos41>=250:
		targ41 = (60 - (6/25)*pos41)*(1.5/60)
	else:
		targ41 = -((6/25)*pos41 - 60)*(0.6/60)
	return targ41


# SIM 2 REAL
def servo12_sim2real(targ12):
	if targ12>=0:
		pos12 = (140 - (targ12/1.2)*65)*(25/6)
	else:
		pos12 = ((abs(targ12)/1)*25 + 140)*(25/6)
	return int(round(pos12))
def servo11_sim2real(targ11):
	if targ11>=0:
		pos11 = ((targ11/1.5)*60 + 180)*(25/6)
	else:
		pos11 = (180 - (abs(targ11)/0.6)*40)*(25/6)
	return int(round(pos11))

def servo32(targ32):
	if targ32>=0:
		pos32 = (140 - (targ32/1.2)*65)*(25/6)
	else:
		pos32 = ((abs(targ32)/1)*25 + 140)*(25/6)
	return int(round(pos32))
def servo31(targ31):
	if targ31>=0:
		pos31 = ((targ31/1.5)*60 + 180)*(25/6)
	else:
		pos31 = (180 - (abs(targ31)/0.6)*40)*(25/6)
	return int(round(pos31))

def servo22(targ22):
	if targ22>=0:
		pos22 = ((targ22/1.2)*65 + 100)*(25/6)
	else:
		pos22 = (100 - (abs(targ22)/1)*25)*(25/6)
	return int(round(pos22))
def servo21(targ21):
	if targ21>=0:
		pos21 = (60 - (targ21/1.5)*60)*(25/6)
	else:
		pos21 = ((abs(targ21)/0.6)*60 + 60)*(25/6)
	return int(round(pos21))

def servo42(targ42):
	if targ42>=0:
		pos42 = ((targ42/1.2)*65 + 100)*(25/6)
	else:
		pos42 = (100 - (abs(targ42)/1)*25)*(25/6)
	return int(round(pos42))
def servo41(targ41):
	if targ41>=0:
		pos41 = (60 - (targ41/1.5)*60)*(25/6)
	else:
		pos41 = ((abs(targ41)/0.6)*60 + 60)*(25/6)
	return int(round(pos41))