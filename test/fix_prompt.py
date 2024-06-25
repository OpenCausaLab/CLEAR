def add_def(data):
  if data["task_type"] == "3_node_relation":
    prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
Given a DAG with three nodes X, Y, Z. 
(1) A "chain" is a sequence of nodes connected by edges where each node has only one predecessor and one successor (except for the first and last nodes in the chain). The simplest chain in a causal graph can be illustrated as "X->Y->Z".
(2) A "fork" refers to a situation where one node has multiple outgoing edges leading to different successor nodes. The simplest fork in a causal graph can be illustrated as "X<-Y->Z".
(3)A "v-structure" means one node is a child of the two others that themselves are not adjacent. The simplest v-structure in a causal graph can be illustrated as "X->Y<-Z".
Question:"""
  elif data["task_type"] == "path":
    prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
A path in a DAG is a sequence of (at least two) distinct nodes i_1,...,i_m such that there is an edge between i_k and i_{k+1} for all k=1,...,m.
Question:"""
  elif data["task_type"] == "blocked_path":
      prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
In a DAG, a path p is said to be blocked by a set of nodes Z if and only if:
(1) p contains a chain i->m->j or a fork i<-m->j such that the middle node m is in Z, or 
(2) p contains an inverted fork (or collider) i->m<-j such that the middle node m is not in Z and such that no descendant of m is in Z.
Question:"""
  elif data["task_type"] == "backdoor_path":
      prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
Given an ordered pair of variables (X, Y), a backdoor path is any path from X to Y that starts with an arrow pointing into X. This backdoor path is a non-causal path from X to Y.
Question:"""
  elif data["task_type"] == "c-component":
      prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
Let G be a causal graph such that a subset of its bidirected arcs forms a spanning tree over all nodes in G. Then G is a C-component.
Question:"""
  elif data["task_type"] == "maximal_root_set":
      prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
Let G be a causal graph and X is one node that belongs to G. If X does not have any descendant, then we call X a root set of G. Maximal root set contains all the root sets of G.
Question:"""
  elif data["task_type"] == "frontdoor_adjustment_set":
      prompt = """You will be provided with a definition of a concept. Using this definition, answer the following question.
Definition: 
If a set of variables Z satisfies the front-door criterion relative to an ordered pair of variables (X, Y):
(1) Z intercepts all directed paths from X to Y;
(2) there is no unblocked back-door path from X to Z; and
(3) all back-door paths from Z to Y are blocked by X.
Then we call Z a frontdoor adjustment set, this set allows us to accurately estimate the causal effect of X on Y.
Question:"""
  else:
      prompt = """ """
  return prompt

def add_1example(data):
####################################  YN  ####################################
    if data["question_type"] == "YN":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Do nodes {C, O, R} form a chain in this graph?
Answer: Yes
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
Is H<-M a path from H to M?
Answer: Yes
Question:"""
        elif data["task_type"] == "blocked_path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes K, S, H, O and directed edges K->O, S->O, K->H, H->O, S->H, K->S.
Can path K->S->O<-H be blocked by nodeset {'S'}?
Answer: Yes
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
Is W<-V->A a backdoor path from W to A?
Answer: Yes
Question:"""
        elif data["task_type"] == "c-component":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given an ADMG (acyclic directed mixed graph) with nodes I, Y, H, U, directed edges I->H, I->Y, I->U, H->U, Y->H and bi-directed edges H<->U, I<->Y.
Is it a C-component?
Answer: No
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
Is {'S'} the maximal root set of this graph?
Answer: Yes
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
Is {'Q'} a valid frontdoor adjustment set for treatment E and outcome P?
Answer: Yes
Question:"""
####################################  MC  ####################################
    elif data["question_type"] == "MC":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Which of the following is a chain of this graph?
A. ('P', 'O', 'C')
B. ('P', 'O', 'R')
C. ('O', 'R', 'C')
D. ('P', 'R', 'C')
Answer: C
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
Which of the following is a path from H to Q?
A. H<-L->Q
B. H<->L<-M->Q
C. H<-M<-L<->Q
D. H->L<-M->Q
Answer: D
Question:"""
        elif data["task_type"] == "blocked_path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes K, S, H, O and directed edges K->O, S->O, K->H, H->O, S->H, K->S.
Which of the following nodesets can block path K->H<-S?
A. set()
B. {'O'}
C. {'H', 'O'}
D. {'H'}
Answer: A
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
Which of the following is a backdoor path from W to L?
A. W->A<-L
B. W<-V->A<-L
C. W<-A<->V->L
D. W->L
Answer: B
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
Which of the following options is the maximal root set of this graph?
A. {'M', 'X'}
B. {'S'}
C. {'M', 'S'}
D. {'J', 'M'}
Answer: B
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
hich of the following sets is a valid frontdoor adjustment set for treatment E and outcome P?
A. set()
B. {'X'}
C. {'Q', 'X'}
D. {'Q'}
Answer: D
Question:"""
####################################  HM  ####################################
    elif data["question_type"] == "HM":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
How many forks does this graph have?
Answer: 1
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
How many paths are there from L to Q?
Answer: 5
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
How many backdoor paths are from node L to node A?
Answer: 2
Question:"""
        elif data["task_type"] == "c-component":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given an ADMG (acyclic directed mixed graph) with nodes I, Y, H, U, directed edges I->H, I->Y, I->U, H->U, Y->H and bi-directed edges H<->U, I<->Y.
It can be uniquely partitioned into a set C(G) of subgraphs, each a maximal C-component. How many subgraphs are there in C(G)?
Answer: 2
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
How many nodes are there in the maximal root set of this graph?
Answer: 1
Question:"""
####################################  EX  ####################################
    elif data["question_type"] == "EX":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Are there any v-structure of this graph?
Answer: No
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with an example and a related question that requires your answer.
Example:
Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
Does there exist a valid frontdoor adjustment set for treatment E and outcome Q?
Answer: No
Question:"""
    else:
        prompt = """ """
    return prompt

def add_3example(data):
####################################  YN  ####################################
    if data["question_type"] == "YN":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with three and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Do nodes {C, O, R} form a chain in this graph?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes P, A, R, T, I and directed edges A->R, A->I, A->T, P->I, P->A, P->T.
Does nodes {T, R, A} form a chain in this graph?
Answer: No

Given a DAG (directed acyclic graph) with nodes Y, S, T, K, C and directed edges Y->S, Y->K, S->T, T->C.
Does nodes {S, K, Y} form a fork in this graph?
Answer: Yes
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
Is H<-M a path from H to M?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes K, M, B, D and directed edges K->M, K->B, B->D, M->B, M->D, K->D.
Is M<-D->K<-B a path from M to B?
Answer: No

Given a DAG (directed acyclic graph) with nodes P, G, K, T, O and directed edges K->T, P->K, G->K, G->O, P->G.
Is T<-K a path from T to K?
Answer: Yes
Question:"""
        elif data["task_type"] == "blocked_path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes K, S, H, O and directed edges K->O, S->O, K->H, H->O, S->H, K->S.
Can path K->S->O<-H be blocked by nodeset {'S'}?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes F, Q, J, E, G, N, T and directed edges E->T, E->N, Q->J, G->T, F->T, G->N, F->J.
Can path G->N<-E->T be blocked by nodeset {'J', 'N'}?
Answer: No

Given a DAG (directed acyclic graph) with nodes K, U, A, Z, Y, D, C, I and directed edges U->I, A->Z, K->A, C->I, A->D, A->I, Z->I, K->Y, Y->C.
Can path A<-K->Y->C->I<-Z be blocked by nodeset {'D', 'I', 'C', 'K'}?
Answer: Yes
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
Is W<-V->A a backdoor path from W to A?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes P, M, I, X, R and directed edges I->R, I->X, M->X, P->M, P->I.
Is I->R a backdoor path from I to R?
Answer: No

Given a DAG (directed acyclic graph) with nodes N, K, T, Q, M, U, W, P, X and directed edges M->U, N->W, Q->X, Q->P, N->K, N->T, Q->U, T->M, N->Q.
Is T<-N->Q->U<-M a backdoor path from T to M?
Answer: Yes
Question:"""
        elif data["task_type"] == "c-component":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given an ADMG (acyclic directed mixed graph) with nodes Q, K, M, Y, directed edges K->Y, K->M, M->Y, Q->K, Q->Y and bi-directed edges K<->Y, Q<->K, Q<->M.
Is it a C-component?
Answer: Yes

Given an ADMG (acyclic directed mixed graph) with nodes I, Y, H, U, directed edges I->H, I->Y, I->U, H->U, Y->H and bi-directed edges H<->U, I<->Y.
Is it a C-component?
Answer: No

Given an ADMG (acyclic directed mixed graph) with nodes W, E, Z, N, directed edges W->Z, E->N, W->N, Z->N and bi-directed edges E<->Z, W<->Z, Z<->N.
Is it a C-component?
Answer: Yes
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
Is {'S'} the maximal root set of this graph?
Answer: Yes

Given an ADMG (acyclic directed mixed graph) with nodes F, O, L, H, M, D, directed edges O->L, M->D, F->L, L->H, F->D, F->O, O->D, L->M and bi-directed edges O<->L.
Is {'M', 'O'} the maximal root set of this graph?
Answer: No

Given an ADMG (acyclic directed mixed graph) with nodes E, P, W, M, U, S, F, H, directed edges P->M, M->F, E->S, S->F, P->H, E->P, W->F, P->W, E->W, W->M, E->F, W->U and bi-directed edges M<->F, E<->M, M<->S, P<->W, W<->H.
Is {'H', 'F', 'U'} the maximal root set of this graph?
Answer: Yes
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
Is {'Q'} a valid frontdoor adjustment set for treatment E and outcome P?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes V, E, M, C, I and directed edges E->M, V->I, M->C, E->I, V->E, V->C.
Is {'M', 'I'} a valid frontdoor adjustment set for treatment E and outcome C?
Answer: No

Given a DAG (directed acyclic graph) with nodes E, U, L, N, C, X and directed edges U->N, E->X, N->C, L->C, E->N, E->U, U->L, L->X.
Is {'L'} a valid frontdoor adjustment set for treatment U and outcome X?
Answer: Yes
Question:"""
####################################  MC  ####################################
    elif data["question_type"] == "MC":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Which of the following is a chain of this graph?
A. ('P', 'O', 'C')
B. ('P', 'O', 'R')
C. ('O', 'R', 'C')
D. ('P', 'R', 'C')
Answer: C

Given a DAG (directed acyclic graph) with nodes W, F, N, O and directed edges F->O, W->F, W->O, N->O, F->N.
Which of the following is a v-structure of this graph?
A. ('F', 'N', 'O')
B. ('W', 'F', 'N')
C. ('W', 'F', 'O')
D. ('W', 'N', 'O')
Answer: D

Given a DAG (directed acyclic graph) with nodes I, J, V, Z, O, R and directed edges O->R, V->R, I->J, I->R, V->Z.
Which of the following is a v-structure of this graph?
A. ('V', 'O', 'R')
B. ('I', 'J', 'Z')
C. ('V', 'Z', 'R')
D. ('I', 'V', 'Z')
Answer: A
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
Which of the following is a path from H to Q?
A. H<-L->Q
B. H<->L<-M->Q
C. H<-M<-L<->Q
D. H->L<-M->Q
Answer: D

Given a DAG (directed acyclic graph) with nodes P, G, K, T, O and directed edges K->T, P->K, G->K, G->O, P->G.
Which of the following is a path from K to O?
A. K<-G->O
B. K->G<->O
C. K<-T<-G<-P<-O
D. K->T->G<-P<->O
Answer: A

Given a DAG (directed acyclic graph) with nodes C, F, S, T, U and directed edges C->F, F->T, F->S, T->U, C->U, C->T, F->U.
Which of the following is a path from C to F?
A. C<->T->F
B. C->T->U<-F
C. C->U->F
D. C->T->F
Answer: B
Question:"""
        elif data["task_type"] == "blocked_path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes K, S, H, O and directed edges K->O, S->O, K->H, H->O, S->H, K->S.
Which of the following nodesets can block path K->H<-S?
A. set()
B. {'O'}
C. {'H', 'O'}
D. {'H'}
Answer: A

Given a DAG (directed acyclic graph) with nodes K, U, A, Z, Y, D, C, I and directed edges U->I, A->Z, K->A, C->I, A->D, A->I, Z->I, K->Y, Y->C.
Which of the following nodesets can block path Y<-K->A->Z->I<-C?
A. {'D', 'I'}
B. {'I', 'A', 'K'}
C. {'I', 'U'}
D. {'I'}
Answer: B

Given a DAG (directed acyclic graph) with nodes Y, U, A, K, M, V, Z, B, P and directed edges M->Z, Y->A, A->K, A->P, K->V, U->V, A->V, Z->B, Y->P, U->M, U->B.
Which of the following nodesets can block path Y->P<-A->V<-K?
A. {'Z', 'B', 'M', 'P', 'V'}
B. {'P', 'V', 'Z', 'U'}
C. {'Z', 'B', 'U', 'P', 'V'}
D. {'V', 'Z', 'B', 'U'}
Answer: D
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
Which of the following is a backdoor path from W to L?
A. W->A<-L
B. W<-V->A<-L
C. W<-A<->V->L
D. W->L
Answer: B

Given an ADMG (acyclic directed mixed graph) with nodes G, K, U, L, directed edges G->L, G->U, G->K, U->L and bi-directed edges K<->L.
Which of the following is a backdoor path from U to L?
A. U->L
B. U<->K->L
C. U<-G->K<->L
D. U<-G<->K<-L
Answer: C

Given an ADMG (acyclic directed mixed graph) with nodes K, F, V, C, directed edges F->C, K->F, V->C and bi-directed edges K<->C.
Which of the following is a backdoor path from F to C?
A. F<-K<->C
B. F->C
C. F->V<->C
D. F<->K->V<->C
Answer: A
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
Which of the following options is the maximal root set of this graph?
A. {'M', 'X'}
B. {'S'}
C. {'M', 'S'}
D. {'J', 'M'}
Answer: B

Given an ADMG (acyclic directed mixed graph) with nodes E, P, W, M, U, S, F, H, directed edges P->M, M->F, E->S, S->F, P->H, E->P, W->F, P->W, E->W, W->M, E->F, W->U and bi-directed edges M<->F, E<->M, M<->S, P<->W, W<->H.
Which of the following options is the maximal root set of this graph?
A. {'E', 'U', 'H', 'P'}
B. {'W', 'S'}
C. {'E', 'W', 'P'}
D. {'H', 'F', 'U'}
Answer: D

Given an ADMG (acyclic directed mixed graph) with nodes Z, K, U, R, P, D, I, A, directed edges U->D, Z->D, K->D, R->D, U->P, R->A, U->R, D->I and bi-directed edges P<->D, I<->A, P<->I.
Which of the following options is the maximal root set of this graph?
A. {'I', 'P', 'A'}
B. {'Z', 'U', 'D'}
C. {'P', 'K', 'Z'}
D. {'K', 'U', 'Z'}
Answer: A
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
hich of the following sets is a valid frontdoor adjustment set for treatment E and outcome P?
A. set()
B. {'X'}
C. {'Q', 'X'}
D. {'Q'}
Answer: D

Given a DAG (directed acyclic graph) with nodes E, U, L, N, C, X and directed edges U->N, E->X, N->C, L->C, E->N, E->U, U->L, L->X.
Which of the following sets is a valid frontdoor adjustment set for treatment U and outcome X?
A. {'C'}
B. {'L'}
C. {'N'}
D. {'C', 'E'}
Answer: B

Given a DAG (directed acyclic graph) with nodes O, J, K, W, M, X, I and directed edges O->I, O->M, J->W, M->I, J->K, W->X, J->I, J->M, W->I, K->X, O->J.
Which of the following sets is a valid frontdoor adjustment set for treatment J and outcome X?
A. {'O', 'W'}
B. {'I'}
C. {'K', 'W'}
D. set()
Answer: C
Question:"""
####################################  HM  ####################################
    elif data["question_type"] == "HM":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
How many forks does this graph have?
Answer: 1

Given a DAG (directed acyclic graph) with nodes E, J, G, H, Q, U and directed edges H->Q, E->U, E->G, E->J, J->U, G->H, G->Q, H->U, G->U.
How many v-structures does this graph have?
Answer: 3

Given a DAG (directed acyclic graph) with nodes H, A, K, J, N, Q, I and directed edges K->Q, H->Q, H->A, K->I, K->J, A->N, H->I, N->Q, A->Q, A->J.
How many chains does this graph have?
Answer: 2
Question:"""
        elif data["task_type"] == "path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes M, H, L, Q and directed edges M->H, H->L, H->Q, L->Q, M->L, M->Q.
How many paths are there from L to Q?
Answer: 5

Given a DAG (directed acyclic graph) with nodes B, O, J, N, Q, H and directed edges N->Q, B->J, O->J, N->H, B->H, B->O.
How many paths are there from N to Q.
Answer: 1

Given a DAG (directed acyclic graph) with nodes H, B, I, M, A, K, Z, C, Y and directed edges B->C, A->K, B->I, B->Y, K->Y, B->K, I->Z, K->C, M->A, H->Y, M->Y.
How many paths are there from I to A.
Answer: 6
Question:"""
        elif data["task_type"] == "backdoor_path":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes V, W, L, A and directed edges W->A, V->W, W->L, V->A, L->A.
How many backdoor paths are from node L to node A?
Answer: 2

Given an ADMG (acyclic directed mixed graph) with nodes N, B, P, H, X, D, J, L, K, directed edges J->K, B->L, B->D, H->D, N->P, P->K, P->X, N->D, N->B, N->H and bi-directed edges X<->D, B<->J.
How many backdoor paths are from node H to node D.
Answer: 5

Given a DAG (directed acyclic graph) with nodes Q, N, F, K and directed edges Q->F, Q->N, N->F, N->K, Q->K.
How many backdoor paths are from node N to node K.
Answer: 1
Question:"""
        elif data["task_type"] == "c-component":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given an ADMG (acyclic directed mixed graph) with nodes I, Y, H, U, directed edges I->H, I->Y, I->U, H->U, Y->H and bi-directed edges H<->U, I<->Y.
It can be uniquely partitioned into a set C(G) of subgraphs, each a maximal C-component. How many subgraphs are there in C(G)?
Answer: 2

Given an ADMG (acyclic directed mixed graph) with nodes K, S, T, G, C, directed edges K->C, S->G, T->C, S->T and bi-directed edges T<->C, G<->C, K<->G, S<->T.
It can be uniquely partitioned into a set C(G) of subgraphs, each a maximal C-component. How many subgraphs are there in C(G)?
Answer: 1

Given an ADMG (acyclic directed mixed graph) with nodes V, Z, R, O, directed edges R->O, Z->O, V->Z, V->R and bi-directed edges Z<->R.
It can be uniquely partitioned into a set C(G) of subgraphs, each a maximal C-component. How many subgraphs are there in C(G)?
Answer: 3
Question:"""
        elif data["task_type"] == "maximal_root_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given an ADMG (acyclic directed mixed graph) with nodes X, J, M, S, directed edges J->S, X->J, M->S, J->M, X->S and bi-directed edges X<->J, M<->S.
How many nodes are there in the maximal root set of this graph?
Answer: 1

Given an ADMG (acyclic directed mixed graph) with nodes Q, G, J, D, O, T, directed edges J->O, D->T, Q->T, J->D, O->T, D->O, Q->J, Q->G, Q->O and bi-directed edges G<->O, O<->T, J<->O, Q<->J, G<->D.
How many nodes are there in the maximal root set of this graph?
Answer: 2

Given an ADMG (acyclic directed mixed graph) with nodes X, V, T, K, P, W, B, J, N, directed edges T->W, V->W, B->N, V->J, V->B, X->J, J->N, X->K, T->J, P->N, X->W and bi-directed edges V<->W, T<->W, V<->J, T<->B, V<->K, X<->J, K<->P, P<->N.
How many nodes are there in the maximal root set of this graph?
Answer: 3
Question:"""
####################################  EX  ####################################
    elif data["question_type"] == "EX":
        if data["task_type"] == "3_node_relation":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes W, F, N, O and directed edges F->O, W->F, W->O, N->O, F->N.
Are there any chain of this graph?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes P, O, R, C and directed edges O->R, P->C, P->O, P->R, R->C.
Are there any v-structure of this graph?
Answer: No

Given a DAG (directed acyclic graph) with nodes E, J, G, H, Q, U and directed edges H->Q, E->U, E->G, E->J, J->U, G->H, G->Q, H->U, G->U.
Are there any fork of this graph?
Answer: Yes
Question:"""
        elif data["task_type"] == "frontdoor_adjustment_set":
            prompt = """You will be provided with three examples and a related question that requires your answer.
Examples:
Given a DAG (directed acyclic graph) with nodes R, T, N, H, X, J, S, I and directed edges T->X, T->J, H->I, N->J, S->I, R->T, T->H, R->N, H->J.
Does there exist a valid frontdoor adjustment set for treatment T and outcome I?
Answer: Yes

Given a DAG (directed acyclic graph) with nodes X, E, Q, P and directed edges Q->P, X->E, X->P, E->Q.
Does there exist a valid frontdoor adjustment set for treatment E and outcome Q?
Answer: No

Given a DAG (directed acyclic graph) with nodes P, U, H, G, I, K, J, N, W and directed edges P->W, J->N, P->N, H->J, I->J, J->W, U->G, N->W, I->K, U->W, P->H.
Does there exist a valid frontdoor adjustment set for treatment H and outcome W?
Answer: Yes
Question:"""
    else:
        prompt = """ """
    return prompt

