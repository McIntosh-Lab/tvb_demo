import sys, os, time, fcntl
import model_montbrio

subject = sys.argv[1:][0]
noise = float(sys.argv[1:][1])
G = float(sys.argv[1:][2])

model_montbrio.process_sub(subject,noise,G) 
