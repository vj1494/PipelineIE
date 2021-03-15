import nltk
import re
from stanza.server import CoreNLPClient


class SentenceSimplify:

    def __init__(self,sentences,annotator,memory,timeout):
        self.sentences = sentences
        self.annotator = annotator
        self.memory = memory
        self.timeout = timeout

    def get_verb_phrases(self,t):
        verb_phrases = []
        num_children = len(t)
        num_VP = sum(1 if t[i].label() == "VP" else 0 for i in range(0, num_children))

        if t.label() != "VP":
            for i in range(0, num_children):
                if t[i].height() > 2:
                    verb_phrases.extend(self.get_verb_phrases(t[i]))
        elif t.label() == "VP" and num_VP > 1:
            for i in range(0, num_children):
                if t[i].label() == "VP":
                    if t[i].height() > 2:
                        verb_phrases.extend(self.get_verb_phrases(t[i]))
        else:
            verb_phrases.append(' '.join(t.leaves()))

        return verb_phrases

    def get_pos(self,t):
        vp_pos = []
        sub_conj_pos = []
        num_children = len(t)
        children = [t[i].label() for i in range(0, num_children)]

        flag = re.search(r"(S|SBAR|SBARQ|SINV|SQ)", ' '.join(children))

        if "VP" in children and not flag:
            for i in range(0, num_children):
                if t[i].label() == "VP":
                    vp_pos.append(t[i].treeposition())
        elif not "VP" in children and not flag:
            for i in range(0, num_children):
                if t[i].height() > 2:
                    temp1, temp2 = self.get_pos(t[i])
                    vp_pos.extend(temp1)
                    sub_conj_pos.extend(temp2)
        else:
            for i in range(0, num_children):
                if t[i].label() in ["S", "SBAR", "SBARQ", "SINV", "SQ"]:
                    temp1, temp2 = self.get_pos(t[i])
                    vp_pos.extend(temp1)
                    sub_conj_pos.extend(temp2)
                else:
                    sub_conj_pos.append(t[i].treeposition())

        return (vp_pos, sub_conj_pos)

    def get_clause_list(self,ann):
        sent_tree = nltk.tree.ParentedTree.fromstring(ann["sentences"][0]["parse"])
        clause_level_list = ["S", "SBAR", "SBARQ", "SINV", "SQ"]
        clause_list = []
        sub_trees = []
        for sub_tree in reversed(list(sent_tree.subtrees())):
            if sub_tree.label() in clause_level_list:
                if sub_tree.parent().label() in clause_level_list:
                    continue

                if (len(sub_tree) == 1 and sub_tree.label() == "S" and sub_tree[0].label() == "VP"
                        and not sub_tree.parent().label() in clause_level_list):
                    continue

                sub_trees.append(sub_tree)
                del sent_tree[sub_tree.treeposition()]

        # for each clause level subtree, extract relevant simple sentence
        for t in sub_trees:
            # get verb phrases from the new modified tree
            verb_phrases = self.get_verb_phrases(t)

            # get tree without verb phrases (mainly subject)
            # remove subordinating conjunctions
            vp_pos, sub_conj_pos = self.get_pos(t)
            for i in vp_pos:
                del t[i]
            for i in sub_conj_pos:
                del t[i]

            subject_phrase = ' '.join(t.leaves())

            # update the clause_list
            for i in verb_phrases:
                clause_list.append(subject_phrase + " " + i)

        clause_list.reverse()
        return clause_list

    def sentence_simplify(self):
        decomposed_sent = []
        with CoreNLPClient(annotators=self.annotator, timeout=self.timeout, memory=self.memory, output_format = 'json') as client:
            for sentence in self.sentences:
                sentence = re.sub(r"(\.|,|\?|\(|\)|\[|\])", " ", sentence)
                ann = client.annotate(sentence)
                clause_list = self.get_clause_list(ann)
                if not clause_list:
                    decomposed_sent.append(sentence)
                else:
                    decomposed_sent.extend(clause_list)
        return decomposed_sent




