all:
	./assembly.py
	./analysis.py

install:
	mkdir data/
	mkdir database/
	mkdir results/
	pip3 install -r requirements.txt
	wget http://spades.bioinf.spbau.ru/release3.7.1/SPAdes-3.7.1-Linux.tar.gz
	# SPAdes installation
	tar -xzf SPAdes-3.7.1-Linux.tar.gz
	rm SPAdes-3.7.1-Linux.tar.gz
	mv SPAdes-3.7.1-Linux/ spades
	# Diamond installation
	wget http://github.com/bbuchfink/diamond/releases/download/v0.7.12/diamond-linux64.tar.gz
	tar xzf diamond-linux64.tar.gz
	rm -r diamond-linux64.tar.gz
	# Krona installation
	wget https://github.com/marbl/Krona/releases/download/v2.6.1/KronaTools-2.6.1.tar
	tar xf KronaTools-2.6.1.tar
	rm KronaTools-2.6.1.tar
	mv KronaTools-2.6.1 krona
	./update_krona.sh
	# Quast installation
	wget https://downloads.sourceforge.net/project/quast/quast-4.0.tar.gz
	tar -xzf quast-4.0.tar.gz
	rm quast-4.0.tar.gz
	mv quast-* quast
	# BWA installation
	wget http://downloads.sourceforge.net/project/bio-bwa/bwakit/bwakit-0.7.12_x64-linux.tar.bz2?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fbio-bwa%2Ffiles%2F&ts=1461241672&use_mirror=freefr
	tar xf bwakit*
	rm bwakit*
	mv bwa.kit bwa_kit

clean:
	rm -rf spades
	rm -rf krona
	rm diamond
	rm -rf quast
	rm -r bwa_kit

restart:
	rm -rf results/*
