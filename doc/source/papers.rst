######
Papers
######

This page collects publications and presentations about PyHDL-IF and
related Python-in-UVM verification topics.

----

Properly Introducing Python To Your UVM Testbench
**************************************************

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - Conference
     - `DVCon US 2026 <https://dvcon.org>`_
   * - Award
     - **Stuart Sutherland Best Paper Award — 1st Place**
   * - Author
     - Matthew Ballance, Advanced Micro Devices (AMD)

**Abstract**

There are many attractive aspects of using Python in a simulation testbench —
including a large ecosystem of libraries and tools.  Among the obstacles is the
integration effort and limitations in the ability to reuse existing UVM content.
This paper presents a UVM-centric integration approach, implemented by an
open-source library, that practically eliminates per-testbench integration work
while preserving the ability to reuse existing UVM assets in a
highly-performant manner.  Examples highlight key use-cases enabled by such an
integration approach.

:download:`Paper (PDF) <papers/ProperlyIntroducingPythonToYourUVMTestbench.pdf>`
| :download:`Presentation slides (PDF) <papers/ProperlyIntroducingPythonToUVM_presentation.pdf>`

----

Refresh Your UVM Testbench with a Spritz of Python
***************************************************

.. list-table::
   :widths: 25 75
   :stub-columns: 1

   * - Conference
     - `62nd ACM/IEEE Design Automation Conference (DAC 2025) <https://www.dac.com>`_ —
       Front-End Design Track
   * - Award
     - **Honorable Mention**
   * - Author
     - Matthew Ballance

**Overview**

This presentation introduces the motivation and key ideas behind blending
Python into an existing SystemVerilog/UVM testbench flow.  It explores why
domain-specific languages (DSLs) such as SystemVerilog cover some verification
tasks extremely well while falling short in areas where general-purpose
languages — and Python in particular — shine.  The talk surveys the trade-offs
of different integration strategies and shows how PyHDL-IF enables practical,
low-overhead Python adoption without discarding existing UVM infrastructure.

:download:`Presentation slides (PDF) <papers/FrontEndTrackSubmission_presentation.pdf>`
