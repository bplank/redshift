#!/usr/bin/env python

import random
import os
import sys
import plac

import redshift.parser
from redshift.parser import GreedyParser, BeamParser, Confusions
import redshift.io_parse


def get_train_str(train_loc, n_sents):
    train_sent_strs = open(train_loc).read().strip().split('\n\n')
    if n_sents != 0:
        random.shuffle(train_sent_strs)
        train_sent_strs = train_sent_strs[:n_sents]
    return '\n\n'.join(train_sent_strs)
 

@plac.annotations(
    train_loc=("Training location", "positional"),
    beam_width=("Beam width", "option", "k", int),
    train_oracle=("Training oracle [static, dyn]", "option", "a", str),
    n_iter=("Number of Perceptron iterations", "option", "i", int),
    feat_thresh=("Feature pruning threshold", "option", "f", int),
    allow_reattach=("Allow Left-Arc to override heads", "flag", "r", bool),
    allow_reduce=("Allow reduce when no head is set", "flag", "d", bool),
    seed=("Set random seed", "option", "s", int),
    n_sents=("Number of sentences to train from", "option", "n", int),
    unlabelled=("Learn unlabelled arcs", "flag", "u", bool),
    # adding confusion matrix
    confusionfile=("confusion file", "option", "c", str)
)
def main(train_loc, model_loc, train_oracle="static", n_iter=15, beam_width=1,
         feat_thresh=10, allow_reattach=False, allow_reduce=False, unlabelled=False,
         n_sents=0, seed=0,confusionfile=None):

    cm=None #confusion object
    if confusionfile:
        confusioninput=[]
        possible_labels=set()
        print >>sys.stderr, "Reading confusion file... ",
        for line in open(confusionfile):
            try:
                if line.startswith("#"):
                    continue
                #row, col, support, norm_over_total, norm_over_row_i, norm_over_row_i_and_col_j
                lab1,lab2,count,norm_over_total, norm_over_row_i, norm_over_row_i_and_col_j=line.strip().split("\t")
                possible_labels.add(lab1)
                possible_labels.add(lab2)
                #confusioninput.append([lab1,lab2,val])
                confusioninput.append([lab1,lab2,count,norm_over_total, norm_over_row_i, norm_over_row_i_and_col_j])
            except IOError:
                print >>sys.stderr, "Not in valid format: confusion file"
                exit()
            cm = Confusions()
            cm.readConfusions(confusioninput,list(possible_labels))
            print cm

        print >>sys.stderr, "Done."


    random.seed(seed)
    if beam_width >= 2:
        parser = BeamParser(model_loc, clean=True,
                            train_alg=train_oracle,
                            feat_thresh=feat_thresh, allow_reduce=allow_reduce,
                            allow_reattach=allow_reattach, beam_width=beam_width,confusions=cm)
    else:
        parser = GreedyParser(model_loc, clean=True, train_alg=train_oracle,
                              feat_thresh=feat_thresh,
                              allow_reduce=allow_reduce,
                              allow_reattach=allow_reattach,confusions=cm)
    train_str = get_train_str(train_loc, n_sents)
    train_data = redshift.io_parse.read_conll(train_str, unlabelled=unlabelled)
    print train_data
    parser.train(train_data, n_iter=n_iter)
    parser.save()


if __name__ == "__main__":
    plac.call(main)
