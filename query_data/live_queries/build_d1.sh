#!/bin/sh

cat d1_splits/datasets_splits.* > tmp.tar.gz
tar -zxvf tmp.tar.gz
mv tmp/* ./
rm tmp -r
rm tmp.tar.g*