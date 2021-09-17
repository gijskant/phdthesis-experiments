#! /usr/bin/env bash

if [ -x "$(which dot)" ]; then
  SKIP_DOT=false
else
  echo "dot not available, not generating images"
  SKIP_DOT=true
fi

run_example() {
  spec="$1"
  echo -e "\nExample: ${spec}"
  mcrl22lps "mcrl2/${spec}.mcrl2" "output/${spec}.lps" && \
  lps2lts "output/${spec}.lps" "output/${spec}.lts" && \
  lps2lts "output/${spec}.lps" "output/${spec}.aut" && \
  ltsconvert "output/${spec}.lts" "output/${spec}.dot" && \
  ltsinfo "output/${spec}.lts" && \
  ($SKIP_DOT || {
    dot -Tpng "-oimages/${spec}.png" "output/${spec}.dot"
    dot -Tpdf "-oimages/${spec}.pdf" "output/${spec}.dot"
  })
}

mkdir -p output

run_example listbuffer
run_example buffer
run_example buffers2

echo -e "\nChecking for weak bisimulation of buffers2 and listbuffer"
lpsbisim2pbes output/buffers2.lps output/listbuffer.lps --bisimulation=weak-bisim output/buffers2-listbuffers-bisim.pbes && \
pbessolve -v output/buffers2-listbuffers-bisim.pbes
