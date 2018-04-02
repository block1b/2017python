# ex: set ro:
# DO NOT EDIT.
# generated by smc (http://smc.sourceforge.net/)
# from file : a.sm

import statemap


class TransitionState(statemap.State):

    def Entry(self, fsm):
        pass

    def Exit(self, fsm):
        pass

    def next_char(self, fsm, c):
        self.Default(fsm)

    def Default(self, fsm):
        msg = "\n\tState: %s\n\tTransition: %s" % (
            fsm.getState().getName(), fsm.getTransition())
        raise statemap.TransitionUndefinedException(msg)

    def getTransitions(self):
        return self._transitions


class Transition_Default(TransitionState):
    _transitions = dict(
        next_char=0,
    )


class Transition_WaitHead(Transition_Default):

    def Entry(self, fsm):
        ctxt = fsm.getOwner()
        ctxt.data_init()

    def next_char(self, fsm, c):
        ctxt = fsm.getOwner()
        if c == "7E" or c == "7e":
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        else:
            fsm.getState().Exit(fsm)
            # No actions.
            pass
            fsm.setState(Transition.WaitHead)
            fsm.getState().Entry(fsm)

    _transitions = dict(
        next_char=1,
    )


class Transition_StartRecv(Transition_Default):

    def next_char(self, fsm, c):
        ctxt = fsm.getOwner()
        if c == "7d" or c == "7D":
            fsm.getState().Exit(fsm)
            # No actions.
            pass
            fsm.setState(Transition.Escape)
            fsm.getState().Entry(fsm)
        elif c == "7E" or c == "7e":
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.gc()
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == 1 and ctxt.getMSG_len() == 0:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == 2 and ctxt.getMSG_len() == 0:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
                ctxt.calcLen()
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == ctxt.getMSG_len() + 3:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
                ctxt.collect()
            finally:
                fsm.setState(Transition.WaitHead)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() < ctxt.getMSG_len() + 3:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        else:
            Transition_Default.next_char(self, fsm, c)

    _transitions = dict(
        next_char=1,
    )


class Transition_Escape(Transition_Default):

    def Entry(self, fsm):
        ctxt = fsm.getOwner()
        ctxt.set_status()

    def next_char(self, fsm, c):
        ctxt = fsm.getOwner()
        if c == "7E" or c == "7e":
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.gc()
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == 1 and ctxt.getMSG_len() == 0:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == 2 and ctxt.getMSG_len() == 0:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
                ctxt.calcLen()
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() == ctxt.getMSG_len() + 3:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
                ctxt.collect()
            finally:
                fsm.setState(Transition.WaitHead)
                fsm.getState().Entry(fsm)
        elif ctxt.getLength() < ctxt.getMSG_len() + 3:
            fsm.getState().Exit(fsm)
            fsm.clearState()
            try:
                ctxt.append(c)
            finally:
                fsm.setState(Transition.StartRecv)
                fsm.getState().Entry(fsm)
        else:
            Transition_Default.next_char(self, fsm, c)

    _transitions = dict(
        next_char=1,
    )


class Transition(object):
    WaitHead = Transition_WaitHead('Transition.WaitHead', 0)
    StartRecv = Transition_StartRecv('Transition.StartRecv', 1)
    Escape = Transition_Escape('Transition.Escape', 2)
    Default = Transition_Default('Transition.Default', -1)


class Transition_sm(statemap.FSMContext):

    def __init__(self, owner):
        statemap.FSMContext.__init__(self, Transition.WaitHead)
        self._owner = owner

    def __getattr__(self, attrib):
        def trans_sm(*arglist):
            self._transition = attrib
            getattr(self.getState(), attrib)(self, *arglist)
            self._transition = None

        return trans_sm

    def enterStartState(self):
        self._state.Entry(self)

    def getOwner(self):
        return self._owner

    _States = (
        Transition.WaitHead,
        Transition.StartRecv,
        Transition.Escape,
    )

    def getStates(self):
        return self._States

    _transitions = (
        'next_char',
    )

    def getTransitions(self):
        return self._transitions

# Local variables:
#  buffer-read-only: t
# End: