EXEC_PY="./exec-py.py"

test: unittests apptests

######################################################################
#
# app-tests
#

APP_SIMS= holdem \
	omaha \
	omahahilo \
	fivecardstudhilo

apptests: $(APP_SIMS)

$(APP_SIMS):
	@echo "Running $@ simulation:"
	@$(EXEC_PY) apps/poker-sim.py -g $@

######################################################################
#
# unittests
#

# List in order to be tested
UNITTESTS = test-Cards \
	test-Hand \
	test-Hands \
	test-PokerRank \
	test-PokerGame

unittests: $(UNITTESTS)

$(UNITTESTS):
	@echo "$@:"
	@$(EXEC_PY) unittests/$@.py

######################################################################
#
# profiles
#

profile-holdem:
	@$(EXEC_PY) profile/$@.py


