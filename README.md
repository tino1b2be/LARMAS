# LARMAS (LAnguage Resource MAnagement System)
Thesis Project for final semester of my BSc.Eng Degree

_Extract from report:_

## Problem Statement
Human language processing systems require large amounts of speech, text and sign-language data to be stored and processed efficiently. Therefore, there is need for a way to efficiently collect, store and access language resources for natural language processing.

##	Problems with current approaches
The problems faced with current approaches to collection and management of speech and text resources are:
*	Not enough data. Acoustic Models and Language Models are used in ASR to statistically represent phonemes (for the former) and word sequences (for the latter). These are built using the language’s speech corpus. The larger this corpus is, the more accurate the ASR engine will be for speech-to-text translations. Unfortunately, open-source speech corpora are not large enough to create accurate acoustic and language models.
*	Restricted access to language resources. Most ASR and other NLP, including open-source ones, have very limited access to the language resources they use. In most cases, this is because the resources would have been licensed to them by third party suppliers who put restrictions on direct access to these resources.
*	Current data collection methods are not scalable. Current data collection methods have a simple architecture that can be described as:
    *	Clients upload the raw recordings to a server.
    *	Researchers manually process these recordings to make sure they are valid for their needs.
    *	The recordings are formatted and stored in a database.

  These approaches work for small scale data collection for research purposes but it is very slow and inefficient for large scale data collection. There are bottlenecks at the receiving end where researchers have to manually process the raw files and also at the storage of the actual data. They cannot handle large scale collection of data (i.e. if thousands of researchers had participated) and lot of labour is also wasted when the researchers have to go through raw data that is not valid for storage.
*	Current data collection methods are thin-client based. When collecting data for a speech corpora (or video in the case of sign language), every recording must be processed to make sure that it is in the right format, has the right Signal-to-Noise ratio, and that it is transcribed properly (words are aligned to the recording). Current data collections methods do not allow any of these processes to happen on the client-side itself before transmitting the data over to the server for processing and storage. In turn, a lot of the collected data is invalid and internet bandwidth is wasted. Historically, client-side devices (voice recorders and mobile phones) were not powerful enough to perform some of the processing required on the raw data. 

##	Proposed Solution
The aim of this project is to develop an open-source client-server system for language resource management. This system will be used to efficiently collect language resources (corpora, sign-language and text) and will allow easy access to the resources for NLP engines and other front-end clients (mobile, desktop and web applications).

##	Objectives
This project will have the following objectives:
*	Collect language resources for NLT. The system must allow for efficient collection of language resources to be used for NLT. These resources could be text, audio, video or other formats.
*	Fully open-source. To allow for further development by anyone interested in this project, it must be fully open-source. All the tools and resources used in this project will be open-source and the project itself will be licensed under the GNU AGPLv3.
*	Highly scalable. To allow for large scale collection of data, the system should be able to handle the extra load when multiple users are using the system.
*	Unrestricted access to the language resources. Users of this system must have unrestricted access to the resources it manages. Users will include NLP researchers and NLP tools and engines that need access to language resources to function.
*	Must be a smart-client and/or thick-client based system. The system must allow the clients to be able to do some of the processing required on the raw data before it is transmitted to the storage server.
