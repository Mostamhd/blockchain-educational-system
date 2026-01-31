# Thesis Revision Task List

Based on Supervisor Feedback (Call 4 - Mukherjee & Miloš).

## 1. High Priority Formatting & Structure
- [x] **Fix Reference Ordering:**
    - *Action:* Change bibliography style to `unsrt` (Order of Appearance) in `thesis/main.tex`.
- [x] **Reduce Table of Contents Depth:**
    - *Action:* Set `\setcounter{tocdepth}{1}` in `thesis/main.tex` (or preamble) to show only Chapters and Sections (exclude Subsections). Goal: Reduce ToC from 4 pages to ~1-2.

## 2. Diagram & Technical Fixes (Prof. Miloš)
- [x] **Fix Class Diagram (UML):**
    - *Node -> SocketCommunication:* Change relationship to **Composition** (Filled Diamond).
    - *Blockchain -> Block:* Change relationship to **Composition** (Filled Diamond).
    - *TransactionPool:* Add association to `Transaction` class.
    - *AccountModel:* Connect to `Blockchain` class (remove "solitaire" status).
- [x] **Fix Transaction Lifecycle Diagram:**
    - *Action:* Rename from "Flowchart" to **"Activity Diagram"**.
    - *Action:* Standardize shapes (use Rhombus for decisions). Ensure strict UML Activity Diagram compliance.

## 3. Chapter 1 (Introduction)
- [x] **Add Structure Flowchart:**
    - *Action:* Create a visual flowchart showing the Thesis Structure (Technical Platform + Curriculum) and insert into Chapter 1.

## 4. Chapter 2 (Theoretical Framework)
- [x] **Rename Related Works:**
    - *Action:* Rename section "Related Work" to **"Real Life Implementation Examples"**.
- [x] **Add Docker Overview:**
    - *Action:* Add a brief (1 paragraph) overview of Docker. Keep it concise (Miloš's advice).
- [x] **Citation Placement:**
    - *Action:* Move citations to the *beginning* of paragraphs/sentences (e.g., "According to Nakamoto [1]...") rather than bunching them at the end of the section.

## 5. Chapter 6 (Results)
- [x] **Update Table Headers:**
    - *Action:* Rename table columns to "**Using** Proof of Work" and "**Using** Proof of Stake".

## 6. Conclusion
- [x] **Add Future Work:**
    - *Action:* Ensure a dedicated "Future Work" subsection exists (Language migration to Go/Kotlin, etc.).

## 7. Open Questions / Low Priority
- [ ] **Architecture Table:** Mukherjee requested a UTXO vs Account table. Miloš said it's unnecessary. *Decision: Skip unless time permits.*
- [x] **reproof the references list:** Make sure that the references list is right and is indeed targeting the part we're citing it in.

## 8. References
- [ ] **references check:** Ensure all references are correctly used and in the text they do reference the same exact topic we cite.
- [ ] **references format:** Ensure all references are correctly formated with the urls displayed correctly
- [ ] Revise that the article mentioned are published in papers or replace them with real papers.


## 9. Chapter 5
- [ ] **modules structure and content:**: in all of the 5 modules revise that all the modules are correctly structured with the differenct sections written clearly and in an understandable and acadmic way.
- [ ] **module 5:**: Ensure that module 5 content makes sense , maybe also mention IPFS if we are going to use it in chapter 1 otherwise look for alternative tasks.



## 10 IMPORTANT:

- [ ] **ai text reduction:**: try to mimimzie the text writing style from ai like to a more human like style (as much as possible). analyze the regulations for using ai



## 11 note to self.

ask the supervisors to review if the references are correct especially the ones mentioning a book.

ask the coordinator about the exact deadline hour 


# 12 update all the "" to the english one where ˝