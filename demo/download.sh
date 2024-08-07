#!/bin/bash

touch manual_operation_required.txt
mkdir -p 3-text;

while read p; do
  wget https://arxiv.org/src/"$p"/arXiv-"$p".tar.gz -P 1-articles/;
  mkdir -p 2-latex/"$p";
  cd 2-latex/"$p";
  tar -xvzf ../../1-articles/arXiv-"$p".tar.gz '*.tex'
  if [ $(ls -1 | wc -l) == 1 ]; then
	pandoc -s *.tex -o ../../3-text/"$p".txt
  elif test -e "main.tex"; then
	pandoc -s main.tex -o ../../3-text/"$p".txt
  else
	echo "$p" >> ../../manual_operation_required.txt
  fi
  cd ../..
done <doi.txt

cd 3-text;


