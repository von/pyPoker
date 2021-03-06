EXEC_PY="./exec-py.py"

test: unittests apptests

######################################################################
#
# app-tests
#

GAME_SIMS= holdem \
	omaha \
	omahahilo \
	fivecardstud \
	fivecardstudhilo \
	sevencardstud \
	sevencardstudhilo

OTHER_APPS= holdem-best-hand \
	holdem-best-suited-hand \
	holdem-domination \
	board-low-analyze \
	board-flush-analyze \
	omaha8-eval

apptests: game-sims $(OTHER_APPS) sha

game-sims: $(GAME_SIMS)

$(GAME_SIMS):
	@echo "Running $@ simulation:"
	@$(EXEC_PY) apps/poker-sim.py -p -g $@

$(OTHER_APPS):
	@$(EXEC_PY) apps/$@.py

sha:
	@$(EXEC_PY) apps/sha.py -v apps/sha-input

######################################################################
#
# Profiling
#

# Make a copy of all the current profiles in snapshot subdirectory
profile-snapshot:
	@test -d profile/snapshot || mkdir profile/snapshot
	@for profile in profile/*.pstats ; do \
		cp $${profile} profile/snapshot ;\
	done

profiles:
	@for game in $(GAME_SIMS) ; do \
		echo -n Profiling $${game}: ;\
		$(EXEC_PY) apps/poker-sim.py -q -g $${game} \
			-P profile/$${game}.pstats || exit 1;\
		$(EXEC_PY) profile/print-pstats.py -t profile/$${game}.pstats ;\
	done

######################################################################
#
# unittests
#

# List in order to be tested
UNITTESTS = \
	test-testing \
	test-Utils \
	test-Action \
	test-Bitfield \
	test-Cards \
	test-PredefinedCards \
	test-Deck \
	test-Hand \
	test-Hands \
	test-HoldEm \
	test-LowRanker \
	test-Omaha \
	test-FiveCardStud \
	test-SevenCardStud \
	test-PokerRank \
	test-HandGenerator \
	test-Player \
	test-PokerGame \
	test-Ranker

unittests: $(UNITTESTS)

$(UNITTESTS):
	@echo "$@:"
	@$(EXEC_PY) unittests/$@.py

######################################################################
#
# Documentation
#

doc:
	@(cd pyPoker; pydoc -w ./*.py)
	@mv pyPoker/*.html doc/

.PHONY: doc
