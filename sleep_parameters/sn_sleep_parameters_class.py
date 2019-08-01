# function to calculate AASM sleep parameters
# hypnogram is a pandas dataframe with column AASM with following values allowed:
# 'W','N1','N2','N3','R','L','A'
# where L is sometimes set for lights on and A is for artefacts
# epochs are assumed to have a length of 30 seconds = 0.5 min
# Total recording time 	TRT 	the recording time in minutes
# Total sleep time 	TST 	time being in sleepstages NREM1-REM in minutes
# Sleep period time 	SPT 	time from falling asleep to final awakening
# Wake after sleep onset 	WASO 	time awake after falling asleep
# Sleep efficiency 	SE 	TST/TRT * 100 in %
# Sleep onset latency 	SOL 	time from start of the recording to sleep in minutes
# Onset latency 	OL 	time from start of the recording to sleep stage in minutes
# Sleep time per stage 	STNREM1-STREM 	time in a certain sleep stage in minutes
# Relative sleep time 	RSTNREM1 - RSTREM 	percentage of certain sleep stage in total sleep time

from collections import namedtuple

Lights = namedtuple('Lights',['off','on'])
SleepEpochs = namedtuple('SleepEpochs',['sleep_onset','final_awakening','total_sleep'])
SleepStageEpochs = namedtuple('SleepStageEpochs',['R','N1','N2','N3'])

class SleepAnalysis:

    def __init__(self, hypnogram, epochlength_in_sec=30):
        self._hypnogram = hypnogram
        self._epochlength_in_sec = epochlength_in_sec
        self._epochlength_in_min = epochlength_in_sec/60
        self._lights = None
        self._total_recording_time = None
        self._sleep_epochs = None
        self._sleep_onset_epoch = None
        self._sleep_onset_latency = None
        self._final_awakening_epoch = None
        self._total_sleep_time = None
        self._sleep_period_time = None
        self._wake_after_sleep_onset = None
        self._sleep_efficiency = None
        self._sleep_stage_epochs = None
        self._onset_latency = None
        self._sleep_time_per_stage = None
        self._relative_sleep_time_per_stage = None

    # %%
    # a method that is presented to the user like an attribute
    @property
    def lights(self):
        """First epoch with again lights on, starting with zero counting."""

        # check if already calculated
        if self._lights is not None:
            return self._lights

        self._lights = self._calc_lights(self._hypnogram)

        return self._lights

    @staticmethod
    def _calc_lights(hypnogram):
        # get the epochs not indicating lights on or artefacts
        no_light = hypnogram[(hypnogram.AASM != 'L') & (hypnogram.AASM != 'A')]

        # lights_on: first indicating L, starting with zero counting
        if no_light.empty:
            return Lights(
                off=float('nan'),
                on=float('nan')
            )

        return Lights(
            off=no_light.index[0],
            on=no_light.index[len(no_light) - 1] + 1
        )


    # %%
    # a method that is presented to the user like an attribute
    @property
    def total_recording_time(self):
        """Lights out to Lights on in minutes."""

        # check if already calculated
        if self._total_recording_time is not None:
            return self._total_recording_time

        # number of epochs requires +1
        self._total_recording_time = self._calc_total_recording_time(self._epochlength_in_min, self.lights.on, self.lights.off)

        return self._total_recording_time

    @staticmethod
    def _calc_total_recording_time(epochlength_in_min, lights_on, lights_off):
        '''
        returns the recording time in minutes, excluding lights on at begin and end
        :param epochlength_in_min:
        :param lights_on:
        :param lights_off:
        :return: RTR [min]
        '''
        return (lights_on - lights_off)*epochlength_in_min

    # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_epochs(self):
        """First epoch of sleep including lights on"""

        # check if already calculated
        if self._sleep_epochs is not None:
            return self._sleep_epochs

        self._sleep_epochs = self._calc_sleep_epochs(self._hypnogram)

        return self._sleep_epochs

    @staticmethod
    def _calc_sleep_epochs(hypnogram):

        # get the epochs indicating nonrem on or rem
        sleep = hypnogram[(hypnogram.AASM == 'N1') | (hypnogram.AASM == 'N2')
                                 | (hypnogram.AASM == 'N3') | (hypnogram.AASM == 'R')]
        return SleepEpochs(
            sleep_onset=sleep.index[0],
            final_awakening=sleep.index[len(sleep)-1]+1,
            total_sleep=len(sleep)
        )

     # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_onset_latency(self):
        """Minutes from Lights out to sleep in minutes."""

        # check if already calculated
        if self._sleep_onset_latency is not None:
            return self._sleep_onset_latency

        # number of epochs requires +1
        self._sleep_onset_latency = self._calc_sleep_onset_latency(self.sleep_epochs.sleep_onset,self.lights.off,self._epochlength_in_min)
        # self._total_recording_time = (self._lights_on - self._lights_off + 1)*self._epochlength_in_min

        return self._sleep_onset_latency

    @staticmethod
    def _calc_sleep_onset_latency(sleep_onset_epoch, lights_off, epochlength_in_min):

        return (sleep_onset_epoch - lights_off)* epochlength_in_min

    # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_period_time(self):
        """Minutes from Lights out to sleep in minutes."""

        # check if already calculated
        if self._sleep_period_time is not None:
            return self._sleep_period_time

        self._sleep_period_time = self._calc_sleep_period_time(self.sleep_epochs.sleep_onset, self.sleep_epochs.final_awakening, self._epochlength_in_min)

        return self._sleep_period_time

    @staticmethod
    def _calc_sleep_period_time(sleep_onset_epoch,final_awakening_epoch, epochlength_in_min):

        return (final_awakening_epoch - sleep_onset_epoch) * epochlength_in_min

    # %%
    # a method that is presented to the user like an attribute
    @property
    def total_sleep_time(self):
        """Time in sleep stage in minutes."""

        # check if already calculated
        if self._total_sleep_time is not None:
            return self._total_sleep_time

        # number of epochs requires +1
        self._total_sleep_time = self._calc_total_sleep_time(self.sleep_epochs.total_sleep, self._epochlength_in_min)

        return self._total_sleep_time

    @staticmethod
    def _calc_total_sleep_time(total_sleep, epochlength_in_min):

        return total_sleep * epochlength_in_min


    # Total sleep time does not require a static method, as the value is already calculated in sleep_epochs

    # %%
    # a method that is presented to the user like an attribute
    @property
    def wake_after_sleep_onset(self):
        """Time awake after falling asleep in minutes before final awakening."""

        # check if already calculated
        if self._wake_after_sleep_onset is not None:
            return self._wake_after_sleep_onset

        # number of epochs requires +1
        self._wake_after_sleep_onset = self._calc_wake_after_sleep_onset(self._hypnogram, self.sleep_epochs.sleep_onset,
                                                                         self.sleep_epochs.final_awakening, self._epochlength_in_min)

        return self._wake_after_sleep_onset

    @staticmethod
    def _calc_wake_after_sleep_onset(hypnogram, sleep_onset_epoch, final_awakening_epoch, epochlength_in_min):

        sleepPeriod = hypnogram.iloc[sleep_onset_epoch:final_awakening_epoch-1]
        Awakenings = sleepPeriod[sleepPeriod.AASM == 'W']

        return Awakenings.AASM.count() * epochlength_in_min

    # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_efficiency(self):
        """Time awake after falling asleep in minutes before final awakening."""

        # check if already calculated
        if self._sleep_efficiency is not None:
            return self._sleep_efficiency

        # number of epochs requires +1
        self._sleep_efficiency = self._calc_sleep_efficiency(self.total_sleep_time, self.total_recording_time)

        return self._sleep_efficiency

    @staticmethod
    def _calc_sleep_efficiency(total_sleep_time, total_recording_time):

        return total_sleep_time/total_recording_time * 100


    # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_stage_epochs(self):
        """number of epochs in different sleep stages """

        # check if already calculated
        if self._sleep_stage_epochs is not None:
            return self._sleep_stage_epochs

        self._sleep_stage_epochs = self._calc_sleep_stage_epochs(self._hypnogram)

        return self._sleep_stage_epochs

    @staticmethod
    def _calc_sleep_stage_epochs(hypnogram):

        sleep_stages = ['R', 'N1', 'N2', 'N3']

        epochs = [len(hypnogram[(hypnogram.AASM == stage)]) for stage in sleep_stages]
        return SleepStageEpochs(*epochs)

    # %%
    # a method that is presented to the user like an attribute
    @property
    def sleep_time_per_stage(self):
        """number of epochs in different sleep stages """

        # check if already calculated
        if self._sleep_time_per_stage is not None:
            return self._sleep_time_per_stage

        self._sleep_time_per_stage = self._calc_sleep_time_per_stage(self.sleep_stage_epochs,self._epochlength_in_min)

        return self._sleep_time_per_stage

    @staticmethod
    def _calc_sleep_time_per_stage(sleep_stage_epochs,epochlength_in_min):

        return SleepStageEpochs(*[epoch * epochlength_in_min for epoch in sleep_stage_epochs])


    # %%
    # a method that is presented to the user like an attribute
    @property
    def onset_latency(self):
        """number of epochs in different sleep stages """

        # check if already calculated
        if self._onset_latency is not None:
            return self._onset_latency

        self._onset_latency = self._calc_onset_latency(self._hypnogram,self.lights.off,self._epochlength_in_min)

        return self._onset_latency

    @staticmethod
    def _calc_onset_latency(hypnogram,lights_off,epochlength_in_min):
        # list comprehension with conditional: first element of present sleepstage if exists at all
        return SleepStageEpochs(*[hypnogram[hypnogram.AASM == sleepstage].index[0] * epochlength_in_min - lights_off*epochlength_in_min
                                  if len(hypnogram[hypnogram.AASM == sleepstage]) > 0
                                  else float('nan') for sleepstage in ['R','N1','N2','N3']])

   # %%
    # a method that is presented to the user like an attribute
    @property
    def relative_sleep_time_per_stage(self):
        """number of epochs in different sleep stages """

        # check if already calculated
        if self._relative_sleep_time_per_stage is not None:
            return self._relative_sleep_time_per_stage

        self._relative_sleep_time_per_stage = self._calc_relative_sleep_time_per_stage(self.sleep_stage_epochs,self.sleep_epochs.total_sleep)

        return self._relative_sleep_time_per_stage

    @staticmethod
    def _calc_relative_sleep_time_per_stage(sleep_stage_epochs,total_sleep_time):

        return SleepStageEpochs(*[epoch/total_sleep_time*100 for epoch in sleep_stage_epochs])