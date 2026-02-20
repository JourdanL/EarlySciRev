# Guidelines for revision detection

## 1. Introduction
The goal of this annotation campaign is to detect text revisions amid paragraphs originating from computer science scientific papers. A paragraph level revision is defined as a paragraph that is substantially modified  for clarity, simplicity, style and other aspects. To that end, some final paragraphs have been selected and each one of them was provided with one or more original paragraphs that were under comment in the latex file. A final paragraph is a paragraph that is not commented and is suspected to be a revision of an original paragraph(s). 
In this task, we aim to characterize the final paragraphs’ relationship with the suspected original paragraph(s), so that they can be classified as revisions or not down the line.

## 2. Annotation Task 
### 2.1 Definition
Annotators are presented with a pair of paragraphs: an original version composed of one or several paragraphs and a final version. Their task is to answer the following question:

Can the final paragraph be qualified as a revision of the original one(s)?

Annotators must select one of the following labels:

* **YES**: The final paragraph constitute a revision of the original paragraph.
* **NO**: The final paragraph does not constitute a revision (e.g., different scientific content, the idea developed is not the same, introduces too much new information, or does not change the text).

As several original candidates are proposed the annotator can answer Yes  for multiple paragraphs (e.g. in cases of paragraph merging or iterative revision)

### 2.2 Examples
#### 2.2.1 Positive examples

| Original Paragraph        | Final paragraph           |
|---------------------------|---------------------------|
| Therefore, the generalization rapidly decreases after augmentationinterrupted when training with a single background because the learning direction toward generalization about various backgrounds is not helpful to train. On the other hand, the training can have helpwhen their difculty is solved by augmentation, such as Figure 2(b) and Figure 2(c). | Therefore, the generalization rapidly decreases after augmentation is interrupted during training with a single background because the learning direction toward generalization about various backgrounds is not helpful to train. In contrast, the training can help when their difficulty is solved by augmentation (Figure 2(b), 2(c)). |

#### 2.2.2 Negative examples 

| Original Paragraph | Final Paragraph |
|--------------------|-----------------|
| In future research, the multi-mode characteristics will be studied to improve the representativeness of degradation features and the trendability of HI, and transfer learning approaches will be investigated to improve the generalization ability of the proposed framework and extend it to different systems. | Based on the ablation study, it can be concluded that the proposed SkipAE, inner HI-prediction block, and the HI-generating module jointly improve the ability of HI for reliable and accurate prognostics. |

### 2.3 Annotation Procedure and Decision Rules
#### 2.3.1 Annotation Steps
For each pair of paragraphs (original and final), annotators must proceed as follows:

1. Read the final paragraph carefully to understand its scientific content and intent.
2. Read the original paragraph to identify any differences with respect to the final version.
3. Assess whether each original is rephrased in the final paragraph considering aspects such as:
    * grammatical correctness,
    * clarity and readability,
    * fluency and coherence,
    * appropriateness of scientific style.
4. Determine whether the scientific meaning of the paragraph is preserved in the final version.
5. Assign a label (YES or NO) according to the decision rules defined below.

Annotators should base their decision solely on the information contained in the paragraph pair and should not rely on external context. Also, annotators are prohibited to invent things.


#### 2.3.2 Decision Rules
Annotators must apply the following rules when assigning labels:

* Assign YES if at least one of the following conditions are met for a part or the whole paragraph :
    1. The final paragraph is a revised version of the original paragraph, incorporating changes ranging from minor edits to substantial rephrasing.
    2. The final version has been modified through the addition, the substitution or the deletion of ideas or facts.
    3. The revision expands on the same idea with additional or withdrawn details.
    4. The differences between the original and final paragraphs indicate the correction of document processing errors (e.g., parsing issues, segmentation errors, or misaligned paragraphs)

* Assign NO if :
    1. None of the above conditions are met.
    2. If the annotator is unsure whether the revised paragraph constitutes a valid paragraph-level revision.
    3. If there are only equations or code
    4. If the the two paragraphs are the exact same

If presented with multiple commented paragraphs for the same final paragraph, one or more commented paragraph can independently be considered as a revision. Classifying a commented paragraph as a revision does not disqualify the other proposed candidates. The same goes with the negative label : all the commented paragraphs may not qualify as a revision.
