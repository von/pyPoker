EXEC_PY="./exec-py.py"

test: unittests apptests

######################################################################
#
# app-tests
#

GAME_SIMS= holdem \
	omaha \
	omahahilo \
	fivecardstudhilo

OTHER_APPS= holdem-best-hand

apptests: game-sims $(OTHER_APPS) sha

game-sims: $(GAME_SIMS)

$(GAME_SIMS):
	@echo "Running $@ simulation:"
	@$(EXEC_PY) apps/poker-sim.py -p -g $@ -P profile/$@.pstats

$(OTHER_APPS):
	@$(EXEC_PY) apps/$@.py

sha:
	@$(EXEC_PY) apps/sha.py -v apps/sha-input

######################################################################
#
# unittests
#

# List in order to be tested
UNITTESTS = test-Cards \
	test-Hand \
	test-Hands \
	test-PokerRank \
	test-HandGenerator \
	test-PokerGame

unittests: $(UNITTESTS)

$(UNITTESTS):
	@echo "$@:"
	@$(EXEC_PY) unittests/$@.py

